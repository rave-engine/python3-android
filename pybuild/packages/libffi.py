from ..source import CPythonSourceDeps
from ..package import Package
from ..util import target_arch


class LibFFI(Package):
    @property
    def source(self):
        return CPythonSourceDeps(branch='libffi')

    def prepare(self):
        self.run(['autoreconf', '--install', '--verbose', '--force'])

        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
