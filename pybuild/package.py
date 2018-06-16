import importlib
import itertools
import os.path
import pathlib
from typing import Dict, Iterator, List
import urllib.request
import urllib.error

from . import env
from .arch import arm
from .patch import Patch
from .source import Source, GitSource, URLSource
from .util import BASE, run_in_dir, target_arch, _PathType, parse_ndk_revision


class Package:
    BUILDDIR = BASE / 'build'
    DIST_PATH = BUILDDIR / 'dist'

    version: str = None
    source: Source = None
    patches: List[Patch] = []
    dependencies: List[str] = []
    skip_uploading: bool = False

    def __init__(self):
        self.name = type(self).__name__.lower()
        self.arch = target_arch().__class__.__name__
        self.env: Dict[str, _PathType] = {}
        self._ndk = None

        if self.version is None and isinstance(self.source, GitSource):
            self.version = 'git'

        for f in itertools.chain(self.sources, self.patches):
            f.package = self

        for directory in (self.DIST_PATH, self.destdir()):
            directory.mkdir(exist_ok=True, parents=True)

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
        return cls.BUILDDIR / 'target' / cls.__name__.lower()

    def init_build_env(self) -> bool:
        if self.env:
            return False

        HOST_OS = os.uname().sysname.lower()

        if HOST_OS not in ('linux', 'darwin'):
            raise Exception(f'Unsupported system {HOST_OS}')

        self.TOOL_PREFIX = (self.ndk / 'toolchains' /
                            target_arch().ANDROID_TOOLCHAIN /
                            'prebuilt' / f'{HOST_OS}-x86_64')
        CLANG_PREFIX = (self.ndk / 'toolchains' /
                        'llvm' / 'prebuilt' / f'{HOST_OS}-x86_64')

        LLVM_BASE_FLAGS = [
            '-target', target_arch().LLVM_TARGET,
            '-gcc-toolchain', self.TOOL_PREFIX,
        ]

        ARCH_SYSROOT = (self.ndk / 'platforms' /
                        f'android-{env.android_api_level}' /
                        f'arch-{self.arch}' / 'usr')
        UNIFIED_SYSROOT = self.ndk / 'sysroot' / 'usr'

        cflags = ['-fPIC']
        if isinstance(target_arch(), arm):
            cflags += ['-fno-integrated-as']

        self.env.update({
            'ANDROID_API_LEVEL': str(env.android_api_level),

            # Sysroots
            'ARCH_SYSROOT': ARCH_SYSROOT,
            'UNIFIED_SYSROOT': UNIFIED_SYSROOT,

            # Compilers
            'CC': f'{CLANG_PREFIX}/bin/clang',
            'CXX': f'{CLANG_PREFIX}/bin/clang++',
            'CPP': f'{CLANG_PREFIX}/bin/clang -E',

            # Compiler flags
            'CPPFLAGS': LLVM_BASE_FLAGS + [
                f'--sysroot={ARCH_SYSROOT}',
                '-isystem', f'{UNIFIED_SYSROOT}/include',
                '-isystem', f'{UNIFIED_SYSROOT}/include/{target_arch().ANDROID_TARGET}',
                f'-D__ANDROID_API__={env.android_api_level}',
            ],
            'CFLAGS': cflags,
            'CXXFLAGS': cflags,
            'LDFLAGS': LLVM_BASE_FLAGS + [
                '--sysroot=' + str(ARCH_SYSROOT),
                '-pie',
            ],
        })

        for dep in self.dependencies:
            dep_pkg = import_package(dep)
            self.env['CPPFLAGS'].extend(['-I', f'{dep_pkg.destdir()}/usr/include'])
            self.env['LDFLAGS'].extend(['-L', f'{dep_pkg.destdir()}/usr/lib'])

        for prog in ('ar', 'as', 'ld', 'objcopy', 'objdump', 'ranlib', 'strip', 'readelf'):
            self.env[prog.upper()] = self.TOOL_PREFIX / 'bin' / f'{target_arch().ANDROID_TARGET}-{prog}'

        return True

    @property
    def filesdir(self) -> pathlib.Path:
        return BASE / 'mk' / self.name

    def need_download(self) -> bool:
        if not self.source:
            return False
        return not (self.source.source_dir / 'Makefile').exists()

    def run(self, cmd: List[str]) -> None:
        self.source.run_in_source_dir(cmd)

    def run_with_env(self, cmd: List[str]) -> None:
        self.init_build_env()
        self.source.run_in_source_dir(cmd, env=self.env)

    def _check_ndk(self) -> pathlib.Path:
        ndk_path = os.getenv('ANDROID_NDK')
        if not ndk_path:
            raise Exception('Requires environment variable $ANDROID_NDK')
        ndk = pathlib.Path(ndk_path)

        if not (ndk / 'sysroot').exists():
            raise Exception('Requires Android NDK r14 beta1 or above')

        self._ndk = ndk

    @property
    def ndk(self):
        if self._ndk is None:
            self._check_ndk()

        return self._ndk

    def prepare(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError

    def create_tarball(self):
        print(f'Creating {self.tarball_name} in {self.DIST_PATH}...')

        run_in_dir(['tar', '-jcf', self.tarball_path, '.'], cwd=self.destdir())

    @property
    def tarball_name(self):
        ndk_revision = parse_ndk_revision(self.ndk)
        return f'{self.name}-{self.arch}-{self.version}-ndk_{ndk_revision}.tar.bz2'

    @property
    def tarball_path(self):
        return self.DIST_PATH / self.tarball_name

    def upload_tarball(self):
        if self.skip_uploading:
            print(f'Skipping uploading for package {self.name}')
            return
        pass

    def fetch_tarball(self):
        if self.skip_uploading:
            print(f'Skipping fetching package {self.name}')
            return

        if self.tarball_path.exists():
            print(f'Skipping already downloaded {self.tarball_path}...')
            return True

        tarball_url = f'https://dl.chyen.cc/python3-android/{self.tarball_name}'
        try:
            print(f'Downloading {tarball_url}...')
            req = urllib.request.urlopen(tarball_url)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print(f'{tarball_url} is missing. Skipping...')
                return False

            raise

        with open(self.tarball_path, 'wb') as f:
            f.write(req.read())

        run_in_dir(
            ['tar', '-jxf', self.tarball_path],
            cwd=self.destdir())

        return True


def import_package(pkgname: str) -> Package:
    pkgmod = importlib.import_module(f'pybuild.packages.{pkgname}')
    for symbol_name in dir(pkgmod):
        symbol = getattr(pkgmod, symbol_name)
        if type(symbol) == type and symbol_name.lower() == pkgname:
            return symbol()

    # XXX: mypy asks for an explicit `return`. Is it necessary?
    return None


def enumerate_packages() -> Iterator[str]:
    for child in (pathlib.Path(__file__).parent / 'packages').iterdir():
        pkgname, ext = os.path.splitext(os.path.basename(child))
        if ext != '.py':
            continue
        yield pkgname
