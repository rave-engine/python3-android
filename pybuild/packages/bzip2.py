from ..builder import Builder
from ..patch import LocalPatch
from ..source import URLSource
from ..package import Package

bzip2 = Package('bzip2')
main_source = URLSource(bzip2, 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz')
bzip2.sources = [main_source]
bzip2.patches = [
    LocalPatch(main_source, 'makefiles'),
]


class BZip2Builder(Builder):
    source = main_source

    def __init__(self):
        super(BZip2Builder, self).__init__()
        self.env['CFLAGS'] = self.env['CPPFLAGS'] + self.env['CFLAGS']

    def build(self):
        self.run_with_env(['make', 'libbz2.a', 'bzip2', 'bzip2recover'])
        self.run_with_env(['make', 'install', f'PREFIX={self.DESTDIR}/usr'])


bzip2.builder = BZip2Builder()
