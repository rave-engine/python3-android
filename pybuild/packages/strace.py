from ..source import URLSource
from ..package import Package
from ..util import target_arch


class Strace(Package):
    validpgpkeys = ['296D6F29A020808E8717A8842DB5BD89A340AEB7']

    @property
    def source(self):
        return URLSource(f'https://strace.io/files/{self.version}/strace-{self.version}.tar.xz', sig_suffix='.asc')

    def build(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            # https://github.com/android-ndk/ndk/issues/190#issuecomment-299597019
            '--enable-mpers=no',
        ])

        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
