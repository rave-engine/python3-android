from ..source import CPythonSourceDeps
from ..package import Package
from ..util import target_arch


class XZ(Package):
    @property
    def source(self):
        return CPythonSourceDeps(branch='xz')

    def build(self):
        self.run(['autoreconf', '--install', '--verbose', '--force'])

        self.run_with_env([
            'bash', './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
