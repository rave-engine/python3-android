from ..patch import LocalPatch
from ..source import URLSource
from ..package import Package


class BZip2(Package):
    source = URLSource('http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz')
    patches = [
        LocalPatch('makefiles'),
        LocalPatch('ndk-issue399'),
    ]

    def __init__(self):
        super(BZip2, self).__init__()
        self.env['CFLAGS'] = self.env['CPPFLAGS'] + self.env['CFLAGS']

    def build(self):
        self.run_with_env(['make', 'libbz2.a', 'bzip2', 'bzip2recover'])
        self.run_with_env(['make', 'install', f'PREFIX={self.DESTDIR}/usr'])
