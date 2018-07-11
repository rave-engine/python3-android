from .. import env
from ..source import GitSource
from ..package import Package
from ..patch import LocalPatch, RemotePatch
from ..util import target_arch


class Python(Package):
    source = GitSource('https://github.com/python/cpython/')
    patches = [
        # https://bugs.python.org/issue29440
        RemotePatch('https://bugs.python.org/file46517/gdbm.patch'),
        LocalPatch('cppflags'),
        LocalPatch('skip-build'),
    ]

    dependencies = list(env.packages)

    skip_uploading = True

    def init_build_env(self) -> bool:
        if not super().init_build_env():
            return False

        self.env['CONFIG_SITE'] = self.filesdir / 'config.site'

        return True

    def prepare(self):
        self.run(['autoreconf', '--install', '--verbose', '--force'])

        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            # CPython requires explicit --build
            '--build=x86_64-linux-gnu',
            '--disable-ipv6',
            '--with-system-ffi',
            '--with-system-expat',
            '--without-ensurepip',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'altinstall', f'DESTDIR={self.destdir()}'])
