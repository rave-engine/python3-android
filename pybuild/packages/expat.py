from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class Expat(Package):
    version = '2.2.7'
    source = URLSource(f'https://github.com/libexpat/libexpat/releases/download/R_{version.replace(".", "_")}/expat-{version}.tar.bz2', sig_suffix='.asc')
    validpgpkeys = ['3D7E959D89FACFEE38371921B00BC66A401A1600']
    patches = [
        LocalPatch('avoid-unknown-warning-options'),
    ]

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
