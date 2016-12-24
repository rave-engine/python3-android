import os
import pathlib
from typing import List

from . import env
from .util import BASE, tostring, target_arch


class Builder:
    BUILDDIR = BASE / 'build'

    def __init__(self) -> None:
        self.env = {}

        ANDROID_NDK = pathlib.Path(os.getenv('ANDROID_NDK'))
        self.DESTDIR = self.BUILDDIR / 'target'

        HOST_OS = os.uname().sysname.lower()

        self.ANDROID_PLATFORM = target_arch().__class__.__name__

        TOOL_PREFIX = (ANDROID_NDK / 'toolchains' /
                       target_arch().ANDROID_TOOLCHAIN /
                       'prebuilt' / f'{HOST_OS}-x86_64')
        CLANG_PREFIX = (ANDROID_NDK / 'toolchains' /
                        'llvm' / 'prebuilt' / f'{HOST_OS}-x86_64')

        LLVM_BASE_FLAGS = tostring([
            '-target', target_arch().LLVM_TARGET,
            '-gcc-toolchain', TOOL_PREFIX,
        ])

        ARCH_SYSROOT = (ANDROID_NDK / 'platforms' /
                        f'android-{env.android_api_level}' /
                        f'arch-{self.ANDROID_PLATFORM}' / 'usr')
        UNIFIED_SYSROOT = ANDROID_NDK / 'sysroot' / 'usr'

        self.env.update({
            'DESTDIR': self.DESTDIR,
            'ANDROID_API_LEVEL': env.android_api_level,

            # Sysroots
            'ARCH_SYSROOT': ARCH_SYSROOT,
            'UNIFIED_SYSROOT': UNIFIED_SYSROOT,

            # Compilers
            'CC': f'{CLANG_PREFIX}/bin/clang {LLVM_BASE_FLAGS}',
            'CXX': f'{CLANG_PREFIX}/bin/clang++ {LLVM_BASE_FLAGS}',
            'CPP': f'{CLANG_PREFIX}/bin/clang -E {LLVM_BASE_FLAGS}',

            # Compiler flags
            'CPPFLAGS': [
                '--sysroot=' + str(UNIFIED_SYSROOT),
                f'-I{UNIFIED_SYSROOT}/include/{target_arch().ANDROID_TARGET}',
                f'-D__ANDROID_API__={env.android_api_level}',
                f'-I{self.DESTDIR}/usr/include',
            ],
            'CFLAGS': ['-fPIC', '-fno-integrated-as'],
            'CXXFLAGS': ['-fPIC', '-fno-integrated-as'],
            'LDFLAGS': [
                '--sysroot=' + str(ARCH_SYSROOT),
                '-pie',
                f'-L{self.DESTDIR}/usr/lib'
            ],

            # pkg-config
            'PKG_CONFIG_LIBDIR': f'{self.DESTDIR}/usr/lib/pkgconfig',
            'PKG_CONFIG_SYSROOT_DIR': self.DESTDIR,
        })
        if self.ANDROID_PLATFORM == 'mips':
            self.env['CFLAGS'].append('-O2')

        for prog in ('ar', 'as', 'ld', 'objcopy', 'objdump', 'ranlib', 'strip', 'readelf'):
            self.env[prog.upper()] = TOOL_PREFIX / 'bin' / f'{target_arch().ANDROID_TARGET}-{prog}'

    def run(self, cmd: List[str]) -> None:
        self.source.run_in_source_dir(cmd, env=self.env)

    def prepare(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError
