from ..source import URLSource
from ..package import Package
from ..util import target_arch


class XZ(Package):
    version = '5.2.3'
    source = URLSource(f'https://tukaani.org/xz/xz-{version}.tar.gz')

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
