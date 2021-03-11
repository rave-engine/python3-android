import argparse
import os
import pathlib
from dataclasses import dataclass
from typing import Dict, Optional

BASE = pathlib.Path(__file__).resolve().parent
SYSROOT = BASE / 'sysroot'


@dataclass
class Arch:
    ANDROID_TARGET: str
    BINUTILS_PREFIX: Optional[str] = None

    @property
    def binutils_prefix(self) -> str:
        return self.BINUTILS_PREFIX or self.ANDROID_TARGET


ARCHITECTURES = {
    'arm': Arch('armv7a-linux-androideabi', 'arm-linux-androideabi'),
    'arm64': Arch('aarch64-linux-android',),
    'x86': Arch('i686-linux-android',),
    'x86_64': Arch('x86_64-linux-android',),
}

def ndk_unified_toolchain() -> pathlib.Path:
    ndk_path = os.getenv('ANDROID_NDK')
    if not ndk_path:
        raise Exception('Requires environment variable $ANDROID_NDK')
    ndk = pathlib.Path(ndk_path)

    HOST_OS = os.uname().sysname.lower()

    path = ndk / 'toolchains' / 'llvm' / 'prebuilt' / f'{HOST_OS}-x86_64' / 'bin'

    if not path.exists():
        raise Exception('Requires Android NDK r19 or above')

    return path


def env_vars(target_arch_name: str, android_api_level: int) -> Dict[str, str]:
    target_arch = ARCHITECTURES[target_arch_name]

    CLANG_PREFIX = (ndk_unified_toolchain() /
                    f'{target_arch.ANDROID_TARGET}{android_api_level}')

    env = {
        # Compilers
        'CC': f'{CLANG_PREFIX}-clang',
        'CXX': f'{CLANG_PREFIX}-clang++',
        'CPP': f'{CLANG_PREFIX}-clang -E',

        # Compiler flags
        'CPPFLAGS': f'-I{SYSROOT}/usr/include',
        'CFLAGS': '-fPIC',
        'CXXLAGS': '-fPIC',
        'LDFLAGS': f'-L{SYSROOT}/usr/lib -pie',

        # pkg-config settings
        'PKG_CONFIG_SYSROOT_DIR': str(SYSROOT),
        'PKG_CONFIG_LIBDIR': str(SYSROOT / 'usr' / 'lib' / 'pkgconfig'),

        'PYTHONPATH': str(BASE),
    }

    for prog in ('ar', 'as', 'nm', 'objcopy', 'objdump', 'ranlib', 'readelf', 'strip'):
        env[prog.upper()] = str(ndk_unified_toolchain() / f'llvm-{prog}')
    env['ld'] = str(ndk_unified_toolchain() / 'lld')

    return env


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arch', required=True, choices=ARCHITECTURES.keys(), dest='target_arch_name')
    parser.add_argument('--api', required=True, type=int, choices=range(21, 30), dest='android_api_level')
    return parser.parse_known_args()
