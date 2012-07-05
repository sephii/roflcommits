import optparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time

import remote

from git import GitParser
from image import ImageManipulator
from snapshot import DummySnapshot, Snapshot

class Roflcommits:
    HOOKS_DIR = '.git/hooks'
    COMMIT_HOOKS_FILE = os.path.join(HOOKS_DIR, 'post-commit')
    PUSH_HOOKS_FILE = os.path.join(HOOKS_DIR, 'update')

    def __init__(self, font_file, font_size):
        self.font_file = font_file
        self.font_size = font_size

    def _create_hooks_dir(self):
        if not os.path.exists(self.HOOKS_DIR):
            os.mkdir(self.HOOKS_DIR)

    def enable_commit_hook(self, options):
        commit_hook_contents = """#!/usr/bin/env sh
roflcommits snapshot"""

        self._create_hooks_dir()
        with open(self.COMMIT_HOOKS_FILE, 'w') as f:
            f.write(commit_hook_contents)

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

        print 'Created push hooks file %s' % (self.COMMIT_HOOKS_FILE)

    def disable_push_hook(self, options):
        if os.path.exists(self.PUSH_HOOKS_FILE):
            os.remove(self.PUSH_HOOKS_FILE)
        else:
            print 'Push hooks file didn\'t exist so not removed'

    def _get_snapshots_dir(self, dir):
        return os.path.expanduser(os.path.join(dir))

    def _get_snapshot_destination(self, dir):
        gp = GitParser()

        return os.path.join(self._get_snapshots_dir(dir), gp.get_hash('-1')) + '.jpg'

    def snapshot(self, options):
        gp = GitParser()
        sn = Snapshot()

        image_path = sn.snapshot()
        im = ImageManipulator(image_path)
        im.add_text(gp.get_message('-1'), ImageManipulator.POSITION_BOTTOMLEFT,
                self.font_file, self.font_size)
        im.add_text(gp.get_hash('-1')[:10], ImageManipulator.POSITION_TOPRIGHT,
                self.font_file, self.font_size)
        im.save(self._get_snapshot_destination(options.destination))

    def upload(self, options, file=None):
        f = remote.Flickr()

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

    usage = 'foobar'
    opt = optparse.OptionParser(usage=usage, version='%prog')
    opt.add_option('-d', '--destination', dest='destination', help='path to'\
            ' directory that will hold the snapshots', default='~/.roflcommits')
    (options, args) = opt.parse_args()

    rc = Roflcommits(font_file, font_size)

    actions = {
        'enable-commit-hook': rc.enable_commit_hook,
        'disable-commit-hook': rc.disable_commit_hook,
        'enable-push-hook': rc.enable_push_hook,
        'disable-push-hook': rc.disable_push_hook,
        'snapshot': rc.snapshot,
        'upload': rc.upload,
        'snapshot-and-upload': rc.snapshot_upload,
    }

    if not args:
        raise Exception('You must provide an action')

    if args[0] not in actions:
        raise Exception('This action doesn\'t exist')

    actions[args[0]](options)

if __name__ == '__main__':
    main()
