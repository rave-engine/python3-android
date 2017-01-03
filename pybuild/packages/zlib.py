from ..builder import Builder
from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch

zlib = Package('zlib')
main_source = URLSource(zlib, 'http://zlib.net/zlib-1.2.10.tar.gz')
zlib.sources = [main_source]
zlib.patches = [
    LocalPatch(main_source, 'fix-ldflags'),
]


class XZBuilder(Builder):
    source = main_source

    def __init__(self):
        super(XZBuilder, self).__init__()

        self.env.update({
            'CHOST': f'{target_arch().ANDROID_TARGET}-',
            'CFLAGS': self.env['CPPFLAGS'] + self.env['CFLAGS'],
        })

    def prepare(self):
        self.run([
            './configure',
            '--prefix=/usr',
            '--static',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install'])


zlib.builder = XZBuilder()
