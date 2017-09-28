from ..source import GitSource
from ..package import Package
from ..util import target_arch


class LibFFI(Package):
    source = GitSource('https://github.com/libffi/libffi')

    def prepare(self):
        self.run(['./autogen.sh'])

        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
