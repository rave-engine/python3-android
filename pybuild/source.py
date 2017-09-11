import os
import os.path
from pathlib import Path
from typing import Any, Dict, List

from .util import BASE, rmtree, run_in_dir


class Source:
    _TAR_SUFFIXES = ('.tar.gz', '.tar.bz2', '.tar.xz', '.tgz')

    def __init__(self, source_url: str, alias: str=None) -> None:
        self.source_url = source_url
        self.basename = os.path.basename(self.source_url.rstrip('/'))
        self.alias = alias

    @property
    def src_prefix(self) -> str:
        pybuild_src = os.getenv('PYBUILD_SRC')
        if pybuild_src:
            ret = Path(pybuild_src)
            ret.mkdir(exist_ok=True)
            return ret

        return BASE / 'src'

    @property
    def dest(self) -> str:
        if self.alias:
            return self.alias

        folder = self.basename
        for suffix in self._TAR_SUFFIXES:
            if folder.endswith(suffix):
                folder = folder[:-len(suffix)]

        return folder

    @property
    def source_dir(self):
        return self.src_prefix / self.dest

    def run_in_source_dir(self, cmd: List[str], env: Dict[str, Any]=None, mode='run'):
        return run_in_dir(cmd, self.source_dir, env, mode)

    def run_globally(self, cmd: List[str], env: Dict[str, str]=None, mode='run'):
        return run_in_dir(cmd, self.src_prefix, env, mode)

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
    def __init__(self, *args, branch='master', **kwargs):
        super(GitSource, self).__init__(*args, **kwargs)

        self.branch = branch

    def clone(self):
        self.run_globally([
            'git', 'clone', '-b', self.branch, self.source_url, self.dest])

    def update(self):
        self.run_in_source_dir(['git', 'fetch', '--tags', 'origin'])
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
        self.run_in_source_dir(['git', 'checkout', '.'])
