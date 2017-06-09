from ..source import URLSource
from ..package import Package
from ..util import target_arch


class SQLite(Package):
    source = URLSource('https://www.sqlite.org/2017/sqlite-autoconf-3190300.tar.gz')

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.DESTDIR}'])
