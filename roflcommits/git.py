import subprocess

class GitParser:
    RETURN_MODE_CODE = 0
    RETURN_MODE_OUTPUT = 1

    def __init__(self, git_dir=None):
        self.git_dir = git_dir

    def _spawn(self, args, return_mode=RETURN_MODE_OUTPUT):
        cmd = ['git']

        if self.git_dir is not None:
            cmd += ['--git-dir', self.git_dir]

        cmd += args

        if return_mode == self.RETURN_MODE_OUTPUT:
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT).communicate()[0]
            output = output.decode('utf-8')
        else:
            output = subprocess.call(cmd)

        return output

    def get_hash(self, commit):
        return self._spawn(['log', commit, '--pretty=format:%H'])

    def get_message(self, commit):
        return self._spawn(['log', commit, '--pretty=format:%s'])

    def is_git_repository(self):
        code = self._spawn(['status'], self.RETURN_MODE_CODE)

        return code == 0
