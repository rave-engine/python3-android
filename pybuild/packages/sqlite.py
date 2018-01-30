from ..source import URLSource
from ..package import Package
from ..util import target_arch


class SQLite(Package):
    version = '3.22.0'
    _vernum = list(map(int, version.split('.')))
    source = URLSource(f'https://www.sqlite.org/2018/sqlite-autoconf-{_vernum[0] * 10000 + _vernum[1] * 100 + _vernum[2]}00.tar.gz')

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
