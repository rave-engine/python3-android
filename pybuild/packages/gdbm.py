from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class GDBM(Package):
    version = '1.18.1'
    source = URLSource(f'https://ftp.gnu.org/gnu/gdbm/gdbm-{version}.tar.gz', sig_suffix='.sig')
    validpgpkeys = ['325F650C4C2B6AD58807327A3602B07F55D0C732']
    patches = [
        LocalPatch('SIZE_T_MAX'),
    ]

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--enable-libgdbm-compat',
            '--disable-static',
        ])

    def build(self):
        self.run(['make', 'V=1'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
