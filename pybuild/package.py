import importlib
import os.path
import pathlib
from typing import Iterator, List

import requests

from . import env
from .arch import arm, x86, mips, arm64
from .patch import Patch, RemotePatch
from .source import Source, GitSource, URLSource
from .util import BASE, run_in_dir, target_arch


class Package:
    BUILDDIR = BASE / 'build'
    DIST_PATH = BUILDDIR / 'dist'

    version: str = None
    source: Source = None
    extra_sources: List[Source] = []
    patches: List[Patch] = []
    dependencies = []
    skip_uploading: bool = False

    def __init__(self):
        self.name = type(self).__name__.lower()
        self.arch = target_arch().__class__.__name__

        if self.version is None and isinstance(self.source, GitSource):
            self.version = 'git'

        self.init_build_env()

        for patch in self.patches:
            patch.package = self

        self.BUILDDIR.mkdir(exist_ok=True)
        self.DIST_PATH.mkdir(exist_ok=True)

    @property
    def sources(self) -> List[Source]:
        return [self.source] + self.extra_sources + [
            URLSource(patch.url)
            for patch in self.patches if isinstance(patch, RemotePatch)]

    @classmethod
    def destdir(cls) -> pathlib.Path:
        return cls.BUILDDIR / 'target' / cls.__name__.lower()

    def init_build_env(self):
        self.env = {}

        ANDROID_NDK = self._check_ndk()

        HOST_OS = os.uname().sysname.lower()

        if HOST_OS not in ('linux', 'darwin'):
            raise Exception(f'Unsupported system {HOST_OS}')

        self.TOOL_PREFIX = (ANDROID_NDK / 'toolchains' /
                            target_arch().ANDROID_TOOLCHAIN /
                            'prebuilt' / f'{HOST_OS}-x86_64')
        CLANG_PREFIX = (ANDROID_NDK / 'toolchains' /
                        'llvm' / 'prebuilt' / f'{HOST_OS}-x86_64')

        LLVM_BASE_FLAGS = [
            '-target', target_arch().LLVM_TARGET,
            '-gcc-toolchain', self.TOOL_PREFIX,
        ]

        ARCH_SYSROOT = (ANDROID_NDK / 'platforms' /
                        f'android-{env.android_api_level}' /
                        f'arch-{self.arch}' / 'usr')
        UNIFIED_SYSROOT = ANDROID_NDK / 'sysroot' / 'usr'

        cflags = ['-fPIC']
        if isinstance(target_arch(), (arm, x86, mips, arm64)):
            cflags += ['-fno-integrated-as']

        self.env.update({
            'ANDROID_API_LEVEL': env.android_api_level,

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

    @property
    def filesdir(self) -> pathlib.Path:
        return BASE / 'mk' / self.name

    def fresh(self) -> bool:
        return not (self.source.source_dir / 'Makefile').exists()

    def run(self, cmd: List[str]) -> None:
        self.source.run_in_source_dir(cmd)

    def run_with_env(self, cmd: List[str]) -> None:
        self.source.run_in_source_dir(cmd, env=self.env)

    def _check_ndk(self) -> pathlib.Path:
        ndk_path = os.getenv('ANDROID_NDK')
        if not ndk_path:
            raise Exception('Requires environment variable $ANDROID_NDK')
        ndk = pathlib.Path(ndk_path)

        if not (ndk / 'sysroot').exists():
            raise Exception('Requires Android NDK r14 beta1 or above')

        return ndk

    def prepare(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError

    def create_tarball(self):
        tarball_name = f'{self.name}-{self.arch}-{self.version}.tar.bz2'

        print(f'Creating {tarball_name} in {self.DIST_PATH}...')

        run_in_dir(
            ['tar', '-jcf', self.DIST_PATH / tarball_name, '.'],
            cwd=self.destdir())

    def upload_tarball(self):
        if self.skip_uploading:
            print(f'Skipping uploading for package {self.name}')
            return

        bintray_version = f'{self.arch}-{self.version}'
        filename = f'{self.name}-{bintray_version}.tar.bz2'

        bintray_username = os.environ['BINTRAY_USERNAME']
        bintray_api_key = os.environ['BINTRAY_API_KEY']

        print(f'Uploading {filename} to Bintray...')

        with open(f'{self.DIST_PATH}/{filename}', 'rb') as pkg:
            r = requests.put(
                f'https://bintray.com/api/v1/content/{bintray_username}/cpython-bin-deps-android/{filename}',
                data=pkg,
                auth=(bintray_username, bintray_api_key),
                headers={
                    'X-Bintray-Package': self.name,
                    'X-Bintray-Version': bintray_version,
                    'X-Bintray-Publish': '1',
                    'X-Bintray-Override': '1',
                })

            print(f'Uploading result: {r.text}')


def import_package(pkgname: str) -> Package:
    pkgmod = importlib.import_module(f'pybuild.packages.{pkgname}')
    for symbol_name in dir(pkgmod):
        symbol = getattr(pkgmod, symbol_name)
        if type(symbol) == type and symbol_name.lower() == pkgname:
            return symbol()

    # XXX: mypy asks for an explicit `return`. Is it necessary?
    return None


def enumerate_packages() -> Iterator[Package]:
    for child in (pathlib.Path(__file__).parent / 'packages').iterdir():
        pkgname, ext = os.path.splitext(os.path.basename(child))
        if ext != '.py':
            continue
        yield pkgname
