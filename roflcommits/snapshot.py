import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time

class SnapshotFailedError(StandardError):
    pass

class Snapshot:
    def __init__(self, delay=0, device=None, skip_frames=0):
        self.delay = delay
        self.tmpdir = None
        self.device = device
        self.skip_frames = skip_frames

    def __del__(self):
        if self.tmpdir is not None and os.path.exists(self.tmpdir):
            self.cleanup()

    def is_linux(self):
        return platform.system() == 'Linux'

    def is_mac(self):
        return platform.system() == 'Darwin'

    def is_windows(self):
        return platform.system() == 'Windows'

    def cleanup(self):
        shutil.rmtree(self.tmpdir)

    def snapshot(self):
        methods = {
            'Linux': self.snapshot_linux,
            'Darwin': self.snapshot_mac,
            'Windows': self.snapshot_win,
        }

        if platform.system() not in methods:
            raise NotImplementedError('Your platform \'%s\' is not supported yet' %
                    platform.system())

        self.tmpdir = tempfile.mkdtemp()

        for i in range(self.delay, 0, -1):
            sys.stdout.write('%s... ' % i)
            sys.stdout.flush()
            time.sleep(1)

        print 'SMILE!'

        return methods[platform.system()]()

    def snapshot_linux(self):
        frames = self.skip_frames

        cmd = ['mplayer', '-vo', 'jpeg:outdir=%s' % self.tmpdir,
            '-frames', str(frames), 'tv://']

        if self.device is not None:
            cmd += ['-tv', 'device=%s' % device]

        output = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        snapshot_path = os.path.join(self.tmpdir, '%.8d.jpg' % frames)

        if not os.path.exists(snapshot_path):
            raise SnapshotFailedError(output)

        return snapshot_path

    def snapshot_mac(self):
        bin_path = os.path.join(os.path.dirname(__file__), 'bin/imagesnap')
        snapshot_path = os.path.join(self.tmpdir, 'snapshot.jpg')
        cmd = [bin_path, snapshot_path]
        output = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if not os.path.exists(snapshot_path):
            raise SnapshotFailedError(output)

        return snapshot_path

    def snapshot_win(self):
        raise NotImplementedError('Your platform \'%s\' is not supported yet' %
                platform.system())

class DummySnapshot(Snapshot):
    def snapshot(self):
        return 'data/sample.jpg'
