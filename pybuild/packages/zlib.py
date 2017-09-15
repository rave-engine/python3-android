from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class ZLib(Package):
    version = '1.2.11'
    source = URLSource(f'https://zlib.net/zlib-{version}.tar.gz')
    patches = [
        LocalPatch('fix-ldflags'),
    ]

    def __init__(self):
        super(ZLib, self).__init__()

        self.env.update({
            'CHOST': f'{target_arch().ANDROID_TARGET}-',
            'CFLAGS': self.env['CPPFLAGS'] + self.env['CFLAGS'],
        })

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--static',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
