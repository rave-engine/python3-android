import os.path
import shlex
from subprocess import check_call, check_output, run, PIPE
from typing import Any, Dict, List

from .package import Package
from .util import BASE, tostring, rmtree


class Source:
    src_prefix = BASE / 'src'
    _TAR_SUFFIXES = ('.tar.gz', '.tar.xz', '.tgz')

    def __init__(self, package: Package, source_url: str):
        self.package = package
        self.source_url = source_url
        self.basename = os.path.basename(self.source_url.rstrip('/'))

    @property
    def dest(self) -> str:
        folder = self.basename
        for suffix in self._TAR_SUFFIXES:
            if folder.endswith(suffix):
                folder = folder[:-len(suffix)]

        return getattr(self, 'alias', folder)

    @property
    def source_dir(self):
        return self.src_prefix / self.dest

    @staticmethod
    def _run_in_dir(cmd: List[str], cwd: str, env: Dict[str, Any], mode):
        print(f'Running in {os.path.relpath(cwd)}: ' + ' '.join([shlex.quote(str(arg)) for arg in cmd]))
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

    def clean(self):
        raise NotImplementedError


class URLSource(Source):
    def download(self):
        target_name = self.src_prefix / self.basename
        if not target_name.exists():
            self.run_globally(['curl', '-v', '-L', '-O', self.source_url])
        else:
            print(f'{target_name!s} already exists, skipping downloading...')

        for suffix in self._TAR_SUFFIXES:
            if self.basename.endswith(suffix):
                self.run_globally(['tar', '-xvf', self.basename])
                break

    def clean(self):
        rmtree(self.source_dir)


class VCSSource(Source):
    @property
    def already_cloned(self):
        return os.path.isdir(self.source_dir)

    def download(self):
        if self.already_cloned:
            self.update()
            self.checkout()
        else:
            self.clone()


class GitSource(VCSSource):
    def clone(self):
        self.run_globally(['git', 'clone', self.source_url, self.dest])

    def update(self):
        self.run_in_source_dir(['git', 'fetch', '--tags', 'origin'])
        self.run_in_source_dir(['git', 'merge', 'origin/master'])

    def clean(self):
        if not self.already_cloned:
            print(f'{self.dest} not cloned yet, skipping...')
            return

        self.checkout()
        self.run_in_source_dir(['git', 'clean', '-dfx'])

    def checkout(self):
        self.run_in_source_dir(['git', 'checkout', '.'])
