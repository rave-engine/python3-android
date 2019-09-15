from ..source import GitSource
from ..package import BasePackage
from ..util import android_api_level, target_arch


class BZip2Source(GitSource):
    def __init__(self):
        super().__init__('https://gitlab.com/federicomenaquintero/bzip2')

    def get_version(self):
        if not self._version and self.source_dir.exists():
            rev_count = self.run_in_source_dir([
                'git', 'rev-list', '--count', 'HEAD'
            ], mode='result').strip()
            rev = self.run_in_source_dir([
                'git', 'rev-parse', '--short', 'HEAD'
            ], mode='result').strip()
            self._version = f'r{rev_count}.{rev}'

        return self._version


class BZip2(BasePackage):
    source = BZip2Source()

    def prepare(self):
        from ..ndk import ndk

        self.run_with_env([
            'cmake',
            f'-DCMAKE_TOOLCHAIN_FILE={ndk.cmake_toolchain}',
            f'-DANDROID_ABI={target_arch().CMAKE_ANDROID_ABI}',
            f'-DANDROID_PLATFORM=android-{android_api_level()}',
            '-DENABLE_STATIC_LIB=ON',
            '-DENABLE_SHARED_LIB=OFF',
            '-DCMAKE_INSTALL_PREFIX=/usr',
            '.'
        ])

    def build(self):
        self.run_with_env(['make'])
        self.run_with_env(['make', 'install', f'DESTDIR={self.destdir()}'])
