from ..package import Package
from ..patch import LocalPatch
from ..source import URLSource
from ..util import target_arch


class LibUUID(Package):
    version = '2.33.1'
    _version_without_patch = '.'.join(version.split('.')[:2])
    # TODO: enable PGP signature checking
    source = URLSource(f'https://www.kernel.org/pub/linux/utils/util-linux/v{_version_without_patch}/util-linux-{version}.tar.xz')
    patches = [
        LocalPatch('path_tmp'),
    ]

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--libdir=/usr/lib',
            '--bindir=/usr/bin',
            '--sbindir=/usr/bin',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-all-programs',
            '--enable-libuuid',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
