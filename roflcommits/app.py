#!/usr/bin/env python

import logging
import optparse
import os
import platform
import runpy
import shutil
import stat
import subprocess
import tempfile

import remote

from git import GitParser
from image import ImageManipulator
from roflcommits import __version__
from snapshot import DummySnapshot, Snapshot

class Settings:
    def get_repository_settings(self, path):
        repositories = getattr(self, 'REPOSITORIES', None)
        if repositories is None:
            raise Exception('Settings REPOSITORIES doesn\'t exist')

        if path not in repositories:
            raise Exception('No such repository `%s`' % path)

        if ('flickr' in repositories[path] and
                isinstance(repositories[path]['flickr'], str)):
            repositories[path]['flickr'] = self.FLICKR_ACCOUNTS[repositories[path]['flickr']]

        return repositories[path]

class Roflcommits:
    HOOKS_DIR = '.git/hooks'
    COMMIT_HOOKS_FILE = os.path.join(HOOKS_DIR, 'post-commit')
    PUSH_HOOKS_FILE = os.path.join(HOOKS_DIR, 'update')

    def __init__(self, font_file, font_size, settings_path):
        self.font_file = font_file
        self.font_size = font_size
        self.settings_path = os.path.expanduser(settings_path)

        self.settings = self._load_settings(self.settings_path)

    def _load_settings(self, path):
        settings = Settings()

        try:
            settings_dict = runpy.run_path(path)
        except IOError:
            raise RuntimeError("Config file not found")
        except Exception:
            raise RuntimeError("Unable to parse the config file")

        for (var, val) in settings_dict.iteritems():
            if var == var.upper():
                setattr(settings, var, val)

        return settings

    def _load_repository_settings(self):
        self.repository_settings = self.settings.get_repository_settings(os.getcwd())

    def _create_hooks_dir(self):
        if not os.path.exists('.git'):
            raise Exception('You must run this command from the root of your'
                    ' git repository')
        if not os.path.exists(self.HOOKS_DIR):
            os.mkdir(self.HOOKS_DIR)

    def enable_commit_hook(self, options):
        self._load_repository_settings()

        if 'flickr' in self.repository_settings:
            command = "snapshot-and-upload"
        else:
            command = "snapshot"

        commit_hook_contents = """#!/usr/bin/env sh
roflcommits %s""" % (command)

        self._create_hooks_dir()
        with open(self.COMMIT_HOOKS_FILE, 'w') as f:
            f.write(commit_hook_contents)

        os.chmod(self.COMMIT_HOOKS_FILE,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        print 'Created commit hooks file %s' % (self.COMMIT_HOOKS_FILE)

    def disable_commit_hook(self, options):
        if os.path.exists(self.COMMIT_HOOKS_FILE):
            os.remove(self.COMMIT_HOOKS_FILE)

            print 'Commit hooks file removed'
        else:
            print 'Commit hooks file didn\'t exist so not removed'

    def enable_push_hook(self, options):
        commit_hook_contents = """#!/usr/bin/env sh
roflcommits upload"""

        self._create_hooks_dir()
        with open(self.PUSH_HOOKS_FILE, 'w') as f:
            f.write(commit_hook_contents)

        os.chmod(self.COMMIT_HOOKS_FILE,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        print 'Created push hooks file %s' % (self.COMMIT_HOOKS_FILE)

    def disable_push_hook(self, options):
        if os.path.exists(self.PUSH_HOOKS_FILE):
            os.remove(self.PUSH_HOOKS_FILE)
        else:
            print 'Push hooks file didn\'t exist so not removed'

    def _get_snapshots_dir(self, dir):
        snapshots_dir = getattr(self, '_snapshots_dir', None)

        if not snapshots_dir:
            snapshots_dir = os.path.expanduser(os.path.join(dir,
                self.repository_settings['name']))

            if not os.path.exists(snapshots_dir):
                os.makedirs(snapshots_dir)

            setattr(self, '_snapshots_dir', snapshots_dir)

        return snapshots_dir

    def _get_snapshot_destination(self, dir):
        gp = GitParser()

        return '%s.jpg' % os.path.join(self._get_snapshots_dir(dir), gp.get_hash('-1'))

    def snapshot(self, options):
        self._load_repository_settings()
        gp = GitParser()
        sn = Snapshot(int(options.delay), options.device,
                      int(options.skip_frames))

        image_path = sn.snapshot()
        im = ImageManipulator(image_path)
        im.resize(options.image_size)
        im.add_text(gp.get_message('-1'), ImageManipulator.POSITION_BOTTOMLEFT,
                self.font_file, self.font_size)
        im.add_text(gp.get_hash('-1')[:10], ImageManipulator.POSITION_TOPRIGHT,
                self.font_file, self.font_size)
        im.save(self._get_snapshot_destination(options.destination))

    def upload(self, options, file=None):
        self._load_repository_settings()

        if 'flickr' not in self.repository_settings:
            logging.warning("You used the `snapshot-and-upload` command, but"
                            " there's no flickr account defined for this"
                            " repository")
            return

        f = remote.Flickr(self.repository_settings['flickr'][0],
                          self.repository_settings['flickr'][1])

        if file is None:
            for file in os.listdir(self._get_snapshots_dir(options.destination)):
                file_path = os.path.join(
                        self._get_snapshots_dir(options.destination), file
                )
                title = os.path.splitext(os.path.basename(file))[0]
                print "Roflcommits: uploading %s" % title
                f.upload(file_path, title, category_name='git commits')
                os.remove(file_path)
        else:
            title = os.path.splitext(os.path.basename(file))[0]
            print "Roflcommits: uploading %s" % title
            f.upload(file, title, category_name='git commits')
            os.remove(file)

    def snapshot_upload(self, options):
        self.snapshot(options)

        self.upload(options, self._get_snapshot_destination(options.destination))

def main():
    font_file = os.path.join(os.path.dirname(__file__), 'data/fonts/impact.ttf')
    font_size = 32
    image_size = '640x480'
    skip_frames = 6

    usage = """Usage: %prog [options] command

Available commands:
  enable-commit-hook   \t\tEnables the `snapshot-and-upload` command on each commit
  disable-commit-hook  \t\tDisables the commit hook
  snapshot             \t\tMakes a snapshot and stores it in your ~/.roflcommits/ directory
  upload               \t\tUploads all snapshots in your ~/.roflcommits/ directory on Flickr
  snapshot-and-upload  \t\tTakes a snapshot and upload it to Flickr"""

    opt = optparse.OptionParser(usage=usage, version=__version__)
    opt.add_option('--api-key', dest='api_key', help='your Flickr API key',
            default='')
    opt.add_option('--api-secret', dest='api_secret', help='your Flickr API'
            ' secret', default='')
    opt.add_option('-s', '--delay', dest='delay', help='delay in seconds before'
            ' taking the snapshot', default=0)
    opt.add_option('-d', '--destination', dest='destination', help='path to'
            ' directory that will hold the snapshots (default is ~/.roflcommits)', default='~/.roflcommits')
    opt.add_option('-v', '--device', dest='device', help='Linux only. The'
            ' device to tell mplayer to use to take the snapshot', default=None)
    opt.add_option('--font', dest='font_path', help='path to'
            ' font to use', default=font_file)
    opt.add_option('--font-size', dest='font_size', help='font size to use'
            ', in pt', default=font_size)
    opt.add_option('--image-size', dest='image_size', help='size of the final'
            ' image (syntax YxZ)', default=image_size)
    opt.add_option('--skip-frames', dest='skip_frames', help='(Linux only) the'
            ' number of frames to skip. Usually the webcam takes some time to'
            ' calibrate. Default is %s' % (skip_frames), default=skip_frames)
    (options, args) = opt.parse_args()

    try:
        options.image_size = tuple([int(x) for x in options.image_size.split('x')])
    except ValueError:
        raise Exception('The --image-size argument must contain a YxZ value'
            ' where Y and Z are numeric')

    if len(options.image_size) < 2:
        raise Exception('The --image-size argument must contain a YxZ value')

    rc = Roflcommits(options.font_path, options.font_size, '~/.roflcommitsrc')

    actions = {
        'enable-commit-hook': rc.enable_commit_hook,
        'disable-commit-hook': rc.disable_commit_hook,
        #'enable-push-hook': rc.enable_push_hook,
        #'disable-push-hook': rc.disable_push_hook,
        'snapshot': rc.snapshot,
        'upload': rc.upload,
        'snapshot-and-upload': rc.snapshot_upload,
    }

    if not args:
        opt.print_help()
    elif args[0] not in actions:
        raise Exception('This action doesn\'t exist')
    else:
        actions[args[0]](options)

if __name__ == '__main__':
    main()
