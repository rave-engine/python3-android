from ..builder import Builder
from ..source import URLSource
from ..package import Package
from ..util import target_arch

expat = Package('expat')
main_source = URLSource(expat, 'https://sourceforge.net/projects/expat/files/expat/2.2.0/expat-2.2.0.tar.bz2')
expat.sources = [main_source]


class ExpatBuilder(Builder):
    source = main_source

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.DESTDIR}'])


expat.builder = ExpatBuilder()
