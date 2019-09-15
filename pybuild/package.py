import importlib
import itertools
import os.path
import pathlib
from typing import Dict, Iterator, List, Optional, Sequence, Union

from .patch import Patch
from .source import Source, URLSource, VCSSource
from .util import (
    _PathType,
    android_api_level,
    BASE,
    target_arch,
)


class BasePackage:
    BUILDDIR = BASE / 'build'
    SYSROOT = BUILDDIR / 'sysroot'

    version: Optional[str] = None
    source: Optional[Source] = None
    patches: List[Patch] = []
    dependencies: List[str] = []
    skip_uploading: bool = False

    def __init__(self, will_build: bool = True):
        self.name = type(self).__name__.lower()
        self.arch = target_arch().__class__.__name__
        self.env: Dict[str, Union[_PathType, Sequence[_PathType]]] = {}

        for f in itertools.chain(self.sources, self.patches):
            f.package = self

        for directory in (self.SYSROOT,):
            directory.mkdir(exist_ok=True, parents=True)

        if will_build:
            self.init_build_env()

    def get_version(self):
        return self.version or self.source.get_version()

    @property
    def sources(self) -> List[Source]:
        ret = []
        for source in itertools.chain([self.source], self.patches):
            if source and isinstance(source, Source):
                ret.append(source)
                if source.sig_suffix:
                    ret.append(URLSource(
                        source.source_url + source.sig_suffix))
        return ret

    @classmethod
    def destdir(cls) -> pathlib.Path:
        return cls.SYSROOT

    def init_build_env(self):
        self.env = {
            # Compiler flags
            'CPPFLAGS': [
                f'-I{self.SYSROOT}/usr/include',
            ],
            'LDFLAGS': [
                f'-L{self.SYSROOT}/usr/lib',
                '-fuse-ld=lld',
            ],

            # pkg-config settings
            'PKG_CONFIG_SYSROOT_DIR': self.SYSROOT,
            'PKG_CONFIG_LIBDIR': self.SYSROOT / 'usr' / 'lib' / 'pkgconfig',
        }

    @property
    def filesdir(self) -> pathlib.Path:
        return BASE / 'mk' / self.name

    def need_download(self) -> bool:
        if not self.source:
            return False
        if isinstance(self.source, VCSSource):
            return True
        return not (self.source.source_dir / 'Makefile').exists()

    def run(self, cmd: List[str], *args, **kwargs) -> None:
        assert isinstance(self.source, Source)
        self.source.run_in_source_dir(cmd, *args, **kwargs)

    def run_with_env(self, cmd: List[str]) -> None:
        assert isinstance(self.source, Source)
        self.source.run_in_source_dir(cmd, env=self.env)

    def prepare(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError


class Package(BasePackage):
    def init_build_env(self):
        from .ndk import ndk

        super().init_build_env()

        CLANG_PREFIX = (ndk.unified_toolchain /
                        f'{target_arch().ANDROID_TARGET}{android_api_level()}')

        self.env.update({
            # Compilers
            'CC': f'{CLANG_PREFIX}-clang',
            'CXX': f'{CLANG_PREFIX}-clang++',
            'CPP': f'{CLANG_PREFIX}-clang -E',
        })

        # Compiler flags
        cflags = ['-fPIC']
        self.env.setdefault('CFLAGS', []).extend(cflags)
        self.env.setdefault('CXXFLAGS', []).extend(cflags)
        self.env.setdefault('LDFLAGS', []).append('-pie')

        for prog in ('ar', 'as', 'ld', 'objcopy', 'objdump', 'ranlib', 'strip', 'readelf'):
            self.env[prog.upper()] = ndk.unified_toolchain / f'{target_arch().binutils_prefix}-{prog}'


def import_package(pkgname: str, will_build: bool = True) -> Package:
    pkgmod = importlib.import_module(f'pybuild.packages.{pkgname}')
    for symbol_name in dir(pkgmod):
        symbol = getattr(pkgmod, symbol_name)
        if type(symbol) == type and symbol_name.lower() == pkgname:
            return symbol(will_build=will_build)

    raise Exception(f'Package {pkgname} not found')


def enumerate_packages() -> Iterator[str]:
    for child in (pathlib.Path(__file__).parent / 'packages').iterdir():
        pkgname, ext = os.path.splitext(os.path.basename(child))
        if ext != '.py':
            continue
        yield pkgname
