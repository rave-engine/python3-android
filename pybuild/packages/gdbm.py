from ..source import URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch


class GDBM(Package):
    version = '1.17'
    source = URLSource(f'https://ftp.gnu.org/gnu/gdbm/gdbm-{version}.tar.gz', sig_suffix='.sig')
    patches = [
        RemotePatch('http://git.gnu.org.ua/cgit/gdbm.git/patch/?id=1059526e357da1aa92e5c020332f4b39ceb37503'),
    ]
    validpgpkeys = ['325F650C4C2B6AD58807327A3602B07F55D0C732']

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--enable-libgdbm-compat',
            '--disable-shared',
        ])

    def build(self):
        self.run(['make', 'V=1'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
