from ..builder import Builder
from ..source import URLSource
from ..package import Package
from ..util import target_arch

sqlite = Package('sqlite')
main_source = URLSource(sqlite, 'https://www.sqlite.org/2016/sqlite-autoconf-3150200.tar.gz')
sqlite.sources = [main_source]


class ReadlineBuilder(Builder):
    source = main_source

    def prepare(self):
        self.run([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install'])


sqlite.builder = ReadlineBuilder()
