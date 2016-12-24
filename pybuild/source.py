import os.path
import shlex
from subprocess import check_call, check_output, run, PIPE
from typing import Any, Dict, List

from .package import Package
from .util import BASE, tostring


class Source:
    src_prefix = BASE / 'src'

    def __init__(self, package: Package, source_url: str):
        self.package = package
        self.source_url = source_url
        self.basename = os.path.basename(self.source_url.rstrip('/'))

        folder = self.basename
        for suffix in ('.tar.gz', '.tar.xz', '.tgz'):
            if folder.endswith(suffix):
                folder = folder[:-len(suffix)]
        self.dest = getattr(self, 'alias', folder)

    @property
    def source_dir(self):
        return self.src_prefix / self.dest

    @staticmethod
    def _run_in_dir(cmd: List[str], cwd: str, env: Dict[str, Any], mode):
        print(f'Running in {cwd!r}: ' + ' '.join([shlex.quote(str(arg)) for arg in cmd]))
        real_env = os.environ.copy()
        for key, value in env.items():
            real_env[key] = tostring(value)
        if mode == 'run':
            check_call(cmd, cwd=cwd, env=real_env)
        elif mode == 'result':
            return check_output(cmd, cwd=cwd, env=real_env).decode('utf-8')
        elif mode == 'result_noerror':
            p = run(cmd, stdout=PIPE, stderr=PIPE, cwd=cwd, env=real_env)
            return (b'\n'.join([p.stderr + p.stdout])).decode('utf-8')

    def run_in_source_dir(self, cmd: List[str], env: Dict[str, Any]={}, mode='run'):
        return self._run_in_dir(cmd, self.source_dir, env, mode)

    def run_globally(self, cmd: List[str], env: Dict[str, str]={}, mode='run'):
        return self._run_in_dir(cmd, self.src_prefix, env, mode)

    def download(self):
        raise NotImplementedError

    def fresh(self):
        raise NotImplementedError


class URLSource(Source):
    def download(self):
        self.run_globally(['wget', '--continue', '--timestamping', self.source_url])
        if self.fresh():
            self.run_globally(['tar', '-xvf', self.basename])

    def fresh(self):
        if not self.source_dir.exists():
            return True

        differs = self.run_globally(['tar', '-df', self.basename], mode='result_noerror')
        for line in differs.split('\n'):
            if line == '' or 'Mode differs' in line or 'Uid differs' in line or 'Gid differs' in line:
                continue
            return False
        return True


class VCSSource(Source):
    @property
    def already_cloned(self):
        return os.path.isdir(self.source_dir)

    def download(self):
        if self.already_cloned:
            self.update()
        else:
            self.checkout()


class GitSource(VCSSource):
    def checkout(self):
        self.run_globally(['git', 'clone', self.source_url, self.dest])

    def update(self):
        self.run_in_source_dir(['git', 'fetch', '--tags', 'origin'])
        self.run_in_source_dir(['git', 'merge', 'origin/master'])

    def fresh(self):
        git_status = self.run_in_source_dir(['git', 'status', '--porcelain'], mode='result')
        return git_status.strip() == ''


class MercurialSource(VCSSource):
    def checkout(self):
        self.run_globally(['hg', 'clone', self.source_url, self.dest])

    def update(self):
        self.run_in_source_dir(['hg', 'pull'])
        self.run_in_source_dir(['hg', 'update', '-v'])

    def fresh(self):
        hg_status = self.run_in_source_dir(['hg', 'status'], mode='result')
        return hg_status.strip() == ''
