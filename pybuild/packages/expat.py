from ..source import URLSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch


class Expat(Package):
    version = '2.2.8'
    source = URLSource(f'https://github.com/libexpat/libexpat/releases/download/R_{version.replace(".", "_")}/expat-{version}.tar.bz2', sig_suffix='.asc')
    validpgpkeys = ['3176EF7DB2367F1FCA4F306B1F9B0E909AF37285']
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
