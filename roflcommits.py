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
    pass

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
    im.save('/tmp/foobar.jpg')
    #with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
    #    im.save(tmp.name)

    #    print 'Publishing on flickr...'
    #    f = remote.Flickr()
    #    f.upload(tmp.name, gp.get_hash('-1'), category_name='git commits')

def upload(options):
    pass

if __name__ == '__main__':
    font_file = 'data/fonts/impact.ttf'
    font_size = 32

    usage = 'foobar'
    opt = optparse.OptionParser(usage=usage, version='%prog')
    (options, args) = opt.parse_args()

    actions = {
        'enable-commit-hook': enable_commit_hook,
        'disable-commit-hook': disable_commit_hook,
        'enable-push-hook': enable_push_hook,
        'disable-push-hook': disable_push_hook,
        'snapshot': snapshot,
        'upload': upload,
    }

    if args[0] not in actions:
        raise Exception('This action doesn\'t exist')

    actions[args[0]](options)
