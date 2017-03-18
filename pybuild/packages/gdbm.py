from ..source import URLSource
from ..package import Package
from ..util import target_arch


class GDBM(Package):
    source = URLSource('https://ftp.gnu.org/gnu/gdbm/gdbm-1.13.tar.gz')

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
        self.run(['make', 'install', f'DESTDIR={self.DESTDIR}'])
