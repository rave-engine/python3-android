from ..patch import LocalPatch
from ..source import URLSource
from ..package import Package


class BZip2(Package):
    version = '1.0.6'
    source = URLSource(f'http://www.bzip.org/{version}/bzip2-{version}.tar.gz')
    patches = [
        LocalPatch('makefiles'),
    ]

    def __init__(self):
        super(BZip2, self).__init__()
        self.env['CFLAGS'] = self.env['CPPFLAGS'] + self.env['CFLAGS']

    def build(self):
        self.run_with_env(['make', 'libbz2.a', 'bzip2', 'bzip2recover'])
        self.run_with_env(['make', 'install', f'PREFIX={self.destdir()}/usr'])
