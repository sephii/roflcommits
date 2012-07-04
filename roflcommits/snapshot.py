import os
import platform
import shutil
import subprocess
import tempfile

class Snapshot:
    def __init__(self, delay=0, device=None):
        self.delay = delay
        self.tmpdir = None
        self.device = device

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
            raise Exception('Your platform \'%s\' is not supported yet' %
                    platform.system())

        self.tmpdir = tempfile.mkdtemp()

        for i in range(self.delay, 0, -1):
            sys.stdout.write('%s... ' % i)
            sys.stdout.flush()
            time.sleep(1)

        print 'SMILE!'

        return methods[platform.system()]()

    def snapshot_linux(self):
        frames = '6'

        cmd = ['mplayer', '-vo', 'jpeg:outdir=%s' % self.tmpdir,
            '-frames', frames, 'tv://']

        if self.device is not None:
            cmd += ['-tv', 'device=%s' % device]

        subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        return os.path.join(self.tmpdir, '00000006.jpg')

    def snapshot_mac(self):
        pass

    def snapshot_win(self):
        pass

class DummySnapshot(Snapshot):
    def snapshot(self):
        return 'data/sample.jpg'
