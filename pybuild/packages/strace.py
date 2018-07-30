from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class Strace(Package):
    version = '4.23'
    source = URLSource(f'https://strace.io/files/{version}/strace-{version}.tar.xz', sig_suffix='.asc')
    patches = [
        LocalPatch('signal-headers'),
    ]
    validpgpkeys = ['296D6F29A020808E8717A8842DB5BD89A340AEB7']

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            # https://github.com/android-ndk/ndk/issues/190#issuecomment-299597019
            '--enable-mpers=no',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
