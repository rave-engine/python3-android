from ..source import CPythonSourceDeps
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class ZLib(Package):
    patches = [
        LocalPatch('fix-ldflags'),
    ]

    @property
    def source(self):
        return CPythonSourceDeps(branch='zlib')

    def init_build_env(self):
        super().init_build_env()

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
