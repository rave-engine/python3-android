import os
import os.path
from pathlib import Path
from typing import Any, Dict, List, Optional

from .util import BASE, gpg_verify_file, rmtree, run_in_dir


class Source:
    _TAR_SUFFIXES = ('.tar.gz', '.tar.bz2', '.tar.xz', '.tgz')

    def __init__(self, source_url: str, alias: str = None, sig_suffix: str = None) -> None:
        self.source_url = source_url
        self.basename = os.path.basename(self.source_url.rstrip('/'))
        self.alias = alias
        self.sig_suffix = sig_suffix

    @property
    def src_prefix(self) -> Path:
        pybuild_src = os.getenv('PYBUILD_SRC')
        if pybuild_src:
            ret = Path(pybuild_src)
            ret.mkdir(exist_ok=True)
            return ret

        return BASE / 'src'

    @property
    def dest(self) -> Optional[str]:
        '''
        Return the name of the directory extracted from tarballs
        '''
        if self.alias:
            return self.alias

        return self._dest

    @property
    def _dest(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def source_dir(self):
        if self.dest:
            return self.src_prefix / self.dest

    @property
    def target(self):
        return self.src_prefix / self.basename

    def run_in_source_dir(self, cmd: List[str], env: Dict[str, Any] = None, mode='run'):
        return run_in_dir(cmd, self.source_dir, env, mode)

    def run_globally(self, cmd: List[str], env: Dict[str, str] = None, mode='run'):
        return run_in_dir(cmd, self.src_prefix, env, mode)

    def get_version(self):
        raise NotImplementedError

    def download(self):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError

    def verify(self, validpgpkeys: List[str]):
        if not self.sig_suffix:
            return

        gpg_verify_file(str(self.target) + self.sig_suffix, self.target,
                        validpgpkeys)

    def clean(self):
        raise NotImplementedError


class URLSource(Source):
    @property
    def _dest(self) -> Optional[str]:
        folder = self.basename
        for suffix in self._TAR_SUFFIXES:
            if folder.endswith(suffix):
                return folder[:-len(suffix)]

        return None

    def download(self):
        if not self.target.exists():
            self.run_globally(['curl', '-v', '-L', '-O', self.source_url])
        else:
            print(f'{self.target!s} already exists, skipping downloading...')

    def extract(self):
        for suffix in self._TAR_SUFFIXES:
            if self.basename.endswith(suffix):
                self.run_globally(['tar', '-xvf', self.basename])
                break

    def clean(self):
        if self.source_dir:  # Don't remove standalone files (patches, etc.)
            rmtree(self.source_dir)


class VCSSource(Source):
    @property
    def _dest(self) -> Optional[str]:
        return self.basename

    @property
    def already_cloned(self):
        return os.path.isdir(self.source_dir)

    def download(self):
        if self.already_cloned:
            self.update()
            self.checkout()
        else:
            self.clone()

    def extract(self):
        pass


class GitSource(VCSSource):
    def __init__(self, *args, branch='master', **kwargs):
        super(GitSource, self).__init__(*args, **kwargs)

        self.branch = branch
        self._version = None

    def get_version(self):
        if not self._version and self.source_dir.exists():
            self._version = self.run_in_source_dir([
                'git', 'describe', '--tags'
            ], mode='result').strip()

        return self._version

    def clone(self):
        self.run_globally([
            'git', 'clone', '--single-branch', '-b', self.branch, self.source_url, self.dest])

    def update(self):
        self.run_in_source_dir(['git', 'fetch', '--no-tags', 'origin', self.branch])
        self.run_in_source_dir([
            'git', 'merge', '--ff-only', f'origin/{self.branch}'])

    def clean(self):
        if not self.already_cloned:
            print(f'{self.dest} not cloned yet, skipping...')
            return

        self.checkout()
        self.run_in_source_dir(['git', 'clean', '-dfx'])

    def checkout(self):
        self.run_in_source_dir(['git', 'checkout', self.branch])
        self.run_in_source_dir(['git', 'reset', '.'])
        self.run_in_source_dir(['git', 'checkout', '.'])


class CPythonSourceDeps(GitSource):
    def __init__(self, *args, branch: str, **kwargs):
        super().__init__(
            source_url='https://github.com/python/cpython-source-deps',
            branch=branch)
        self.basename = branch
