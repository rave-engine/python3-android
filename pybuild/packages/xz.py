from ..builder import Builder
from ..source import URLSource
from ..package import Package
from ..util import target_arch

xz = Package('xz')
main_source = URLSource(xz, 'http://tukaani.org/xz/xz-5.2.3.tar.gz')
xz.sources = [main_source]


class XZBuilder(Builder):
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


xz.builder = XZBuilder()
