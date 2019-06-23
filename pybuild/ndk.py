import os
import pathlib


class NDK():
    def __init__(self):
        ndk_path = os.getenv('ANDROID_NDK')
        if not ndk_path:
            raise Exception('Requires environment variable $ANDROID_NDK')
        ndk = pathlib.Path(ndk_path)

        HOST_OS = os.uname().sysname.lower()

        if HOST_OS not in ('linux', 'darwin'):
            raise Exception(f'Unsupported system {HOST_OS}')

        self.unified_toolchain = ndk / 'toolchains' / 'llvm' / 'prebuilt' / f'{HOST_OS}-x86_64' / 'bin'

        if not self.unified_toolchain.exists():
            raise Exception('Requires Android NDK r19 or above')


ndk = NDK()
