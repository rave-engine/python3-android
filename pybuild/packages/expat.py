from ..source import URLSource
from ..package import Package
from ..util import target_arch


class Expat(Package):
    version = '2.2.5'
    source = URLSource(f'https://sourceforge.net/projects/expat/files/expat/{version}/expat-{version}.tar.bz2')

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
