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

def enable_commit_hook(options):
    with open('.git/hooks/post-commit', 'w') as f:
        f.writelines(['#!/usr/bin/env python', '~/private/roflcommits/roflcommits.py snapshot_upload'])

def disable_commit_hook(options):
    pass

def enable_push_hook(options):
    pass

def disable_push_hook(options):
    pass

def snapshot(options):
    gp = GitParser()
    sn = Snapshot()

    image_path = sn.snapshot()
    im = ImageManipulator(image_path)
    im.add_text(gp.get_message('-1'), ImageManipulator.POSITION_BOTTOMLEFT,
            font_file, font_size)
    im.add_text(gp.get_hash('-1')[:10], ImageManipulator.POSITION_TOPRIGHT,
            font_file, font_size)
    print os.path.expanduser(os.path.join(options.destination,
        gp.get_hash('-1')) + '.jpg')
    im.save(os.path.expanduser(os.path.join(options.destination,
        gp.get_hash('-1')) + '.jpg'))
    #with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
    #    im.save(tmp.name)

    #    print 'Publishing on flickr...'
    #    f = remote.Flickr()
    #    f.upload(tmp.name, gp.get_hash('-1'), category_name='git commits')

def upload(options):
    gp = GitParser()
    image = os.path.expanduser(os.path.join(options.destination,
        gp.get_hash('-1')) + '.jpg')
    f = remote.Flickr()
    f.upload(image, gp.get_hash('-1'), category_name='git commits')

def snapshot_upload(options):
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

    actions = {
        'enable-commit-hook': enable_commit_hook,
        'disable-commit-hook': disable_commit_hook,
        'enable-push-hook': enable_push_hook,
        'disable-push-hook': disable_push_hook,
        'snapshot': snapshot,
        'upload': upload,
        'snapshot-and-upload': snapshot_upload,
    }

    if args[0] not in actions:
        raise Exception('This action doesn\'t exist')

    actions[args[0]](options)
