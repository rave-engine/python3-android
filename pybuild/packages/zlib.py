from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class ZLib(Package):
    version = '1.2.11'
    source = URLSource(f'https://zlib.net/zlib-{version}.tar.gz', sig_suffix='.asc')
    validpgpkeys = ['5ED46A6721D365587791E2AA783FCD8E58BCAFBA']
    patches = [
        LocalPatch('fix-ldflags'),
    ]

    def init_build_env(self) -> bool:
        if not super().init_build_env():
            return False

        self.env.update({
            'CHOST': f'{target_arch().ANDROID_TARGET}-',
            'CFLAGS': self.env['CPPFLAGS'] + self.env['CFLAGS'],
        })

        return True

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--static',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
