from ..source import URLSource
from ..package import Package
from ..util import target_arch


class XZ(Package):
    validpgpkeys = ['3690C240CE51B4670D30AD1C38EE757D69184620']

    @property
    def source(self):
        return URLSource(
            f'https://tukaani.org/xz/xz-{self.version}.tar.gz',
            sig_suffix='.sig')

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
