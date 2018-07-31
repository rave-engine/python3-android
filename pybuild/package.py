import importlib
import itertools
import os.path
import pathlib
import shutil
from typing import Dict, Iterator, List, Optional, Sequence, Union
import urllib.request
import urllib.error

from .env import gpg_key_id
from .patch import Patch
from .source import Source, GitSource, URLSource
from .util import (
    _PathType,
    android_api_level,
    BASE,
    gpg_sign_file,
    gpg_verify_file,
    parse_ndk_revision,
    run_in_dir,
    tar_cmd,
    target_arch,
)


class Package:
    BUILDDIR = BASE / 'build'
    DIST_PATH = BUILDDIR / 'dist'
    SYSROOT = BUILDDIR / 'sysroot'
    ARCHIVES_ROOT = 'https://dl.chyen.cc/python3-android/'

    version: Optional[str] = None
    source: Optional[Source] = None
    patches: List[Patch] = []
    dependencies: List[str] = []
    skip_uploading: bool = False

    def __init__(self):
        self.name = type(self).__name__.lower()
        self.arch = target_arch().__class__.__name__
        self.env: Dict[str, Union[_PathType, Sequence[_PathType]]] = {}
        self._ndk = None

        if self.version is None and isinstance(self.source, GitSource):
            self.version = 'git'

        for f in itertools.chain(self.sources, self.patches):
            f.package = self

        for directory in (self.DIST_PATH, self.destdir(), self.SYSROOT):
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
                        f'android-{android_api_level()}' /
                        f'arch-{self.arch}' / 'usr')
        UNIFIED_SYSROOT = self.ndk / 'sysroot' / 'usr'

        cflags = ['-fPIC']

        self.env.update({
            'ANDROID_API_LEVEL': str(android_api_level()),

            # Sysroots
            'ARCH_SYSROOT': ARCH_SYSROOT,
            'UNIFIED_SYSROOT': UNIFIED_SYSROOT,

            # Compilers
            'CC': f'{CLANG_PREFIX}/bin/clang',
            'CXX': f'{CLANG_PREFIX}/bin/clang++',
            'CPP': f'{CLANG_PREFIX}/bin/clang -E',

            # Compiler flags
            'CPPFLAGS': LLVM_BASE_FLAGS + [
                f'-I{self.SYSROOT}/usr/include',
                f'--sysroot={ARCH_SYSROOT}',
                '-isystem', f'{UNIFIED_SYSROOT}/include',
                '-isystem', f'{UNIFIED_SYSROOT}/include/{target_arch().ANDROID_TARGET}',
                f'-D__ANDROID_API__={android_api_level()}',
            ],
            'CFLAGS': cflags,
            'CXXFLAGS': cflags,
            'LDFLAGS': LLVM_BASE_FLAGS + [
                f'-L{self.SYSROOT}/usr/lib',
                '--sysroot=' + str(ARCH_SYSROOT),
                '-pie',
            ],

            # pkg-config settings
            'PKG_CONFIG_SYSROOT_DIR': self.SYSROOT,
            'PKG_CONFIG_LIBDIR': self.SYSROOT / 'usr' / 'lib' / 'pkgconfig',
        })

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
        assert isinstance(self.source, Source)
        self.source.run_in_source_dir(cmd)

    def run_with_env(self, cmd: List[str]) -> None:
        assert isinstance(self.source, Source)
        self.init_build_env()
        self.source.run_in_source_dir(cmd, env=self.env)

    def _check_ndk(self) -> None:
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

        run_in_dir([tar_cmd(), '-jcf', self.tarball_path, '.'], cwd=self.destdir())

        gpg_sign_file(self.tarball_path, gpg_key_id)

    @property
    def tarball_name(self):
        ndk_revision = parse_ndk_revision(self.ndk)
        return f'{self.name}-{self.arch}-{self.version}-android{android_api_level()}-ndk_{ndk_revision}.tar.bz2'

    @property
    def tarball_sig_name(self):
        return self.tarball_name + '.sig'

    @property
    def tarball_path(self):
        return self.DIST_PATH / self.tarball_name

    @property
    def tarball_sig_path(self):
        return self.DIST_PATH / self.tarball_sig_name

    def upload_tarball(self):
        if self.skip_uploading:
            print(f'Skipping uploading for package {self.name}')
            return
        dest = os.getenv('PYTHON3_ANDROID_TARBALL_DEST')
        if dest:
            dest_path = pathlib.Path(dest)
            for filepath in (self.tarball_path, self.tarball_sig_path):
                shutil.copy2(filepath, dest_path)
                # buildbot defaults to umask 077
                os.chmod(dest_path / os.path.basename(filepath), 0o644)

    def verify_tarball(self):
        gpg_verify_file(self.tarball_sig_path, self.tarball_path, [gpg_key_id])

    def extract_tarball(self):
        run_in_dir(
            [tar_cmd(), '-jxf', self.tarball_path],
            cwd=self.SYSROOT)

    def fetch_tarball(self):
        if self.skip_uploading:
            print(f'Skipping fetching package {self.name}')
            return

        if self.tarball_path.exists():
            print(f'Skipping already downloaded {self.tarball_path}...')
            return True

        for file_path in (self.tarball_path, self.tarball_sig_path):
            url = self.ARCHIVES_ROOT + os.path.basename(file_path)
            try:
                print(f'Downloading {url}...')
                req = urllib.request.urlopen(url)
            except urllib.error.HTTPError as err:
                if err.code == 404:
                    print(f'{url} is missing. Skipping...')
                    return False

                raise

            with open(file_path, 'wb') as f:
                f.write(req.read())

        self.verify_tarball()
        self.extract_tarball()

        return True


def import_package(pkgname: str) -> Package:
    pkgmod = importlib.import_module(f'pybuild.packages.{pkgname}')
    for symbol_name in dir(pkgmod):
        symbol = getattr(pkgmod, symbol_name)
        if type(symbol) == type and symbol_name.lower() == pkgname:
            return symbol()

    raise Exception(f'Package {pkgname} not found')


def enumerate_packages() -> Iterator[str]:
    for child in (pathlib.Path(__file__).parent / 'packages').iterdir():
        pkgname, ext = os.path.splitext(os.path.basename(child))
        if ext != '.py':
            continue
        yield pkgname
