from ..source import URLSource
from ..package import Package
from ..util import target_arch


class LibFFI(Package):
    @property
    def source(self):
        return URLSource(
            f'https://github.com/libffi/libffi/releases/download/v{self.version}/libffi-{self.version}.tar.gz')

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
