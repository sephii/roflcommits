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
from snapshot import Snapshot

class Roflcommits:
    HOOKS_DIR = '.git/hooks'
    COMMIT_HOOKS_FILE = os.path.join(HOOKS_DIR, 'post-commit')
    PUSH_HOOKS_FILE = os.path.join(HOOKS_DIR, 'update')

    def _create_hooks_dir(self):
        if not os.path.exists(self.HOOKS_DIR):
            os.mkdir(self.HOOKS_DIR)

    def enable_commit_hook(self, options):
        commit_hook_contents = """#!/usr/bin/env sh
    python ~/private/roflcommits/roflcommits.py snapshot-and-upload"""

        _create_hooks_dir()
        with open(self.COMMIT_HOOKS_FILE, 'w') as f:
            f.write(commit_hook_contents)

    def disable_commit_hook(self, options):
        if os.path.exists(self.COMMIT_HOOKS_FILE):
            os.remove(self.COMMIT_HOOKS_FILE)

    def enable_push_hook(self, options):
        commit_hook_contents = """#!/usr/bin/env sh
    python ~/private/roflcommits/roflcommits.py upload"""

        _create_hooks_dir()
        with open(self.PUSH_HOOKS_FILE, 'w') as f:
            f.write(commit_hook_contents)

    def disable_push_hook(self, options):
        if os.path.exists(self.PUSH_HOOKS_FILE):
            os.remove(self.PUSH_HOOKS_FILE)

    def _get_snapshot_destination(self, dir):
        gp = GitParser()

        return os.path.expanduser(os.path.join(options.destination,
            gp.get_hash('-1')) + '.jpg')

    def snapshot(self, options):
        gp = GitParser()
        sn = Snapshot()

        image_path = sn.snapshot()
        im = ImageManipulator(image_path)
        im.add_text(gp.get_message('-1'), ImageManipulator.POSITION_BOTTOMLEFT,
                font_file, font_size)
        im.add_text(gp.get_hash('-1')[:10], ImageManipulator.POSITION_TOPRIGHT,
                font_file, font_size)
        print _get_snapshot_destination(options.destination)
        im.save(_get_snapshot_destination(options.destination))

    def upload(self, options):
        gp = GitParser()
        image = _get_snapshot_destination(options.destination)
        f = remote.Flickr()
        f.upload(image, gp.get_hash('-1').encode('utf-8'), category_name='git commits')

    def snapshot_upload(self, options):
        snapshot(options)
        upload(options)

if __name__ == '__main__':
    font_file = 'data/fonts/impact.ttf'
    font_size = 32

    usage = 'foobar'
    opt = optparse.OptionParser(usage=usage, version='%prog')
    opt.add_option('-d', '--destination', dest='destination', help='path to'\
            ' directory that will hold the snapshots', default='~/.roflcommits')
    (options, args) = opt.parse_args()

    rc = Roflcommits()

    actions = {
        'enable-commit-hook': rc.enable_commit_hook,
        'disable-commit-hook': rc.disable_commit_hook,
        'enable-push-hook': rc.enable_push_hook,
        'disable-push-hook': rc.disable_push_hook,
        'snapshot': rc.snapshot,
        'upload': rc.upload,
        'snapshot-and-upload': rc.snapshot_upload,
    }

    if args[0] not in actions:
        raise Exception('This action doesn\'t exist')

    actions[args[0]](options)
