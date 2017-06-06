from ..source import GitSource
from ..package import Package
from ..patch import LocalPatch, RemotePatch
from ..util import target_arch


class Python(Package):
    source = GitSource('https://github.com/python/cpython/')
    patches = [
        # http://bugs.python.org/issue29440
        RemotePatch('http://bugs.python.org/file46517/gdbm.patch'),
        LocalPatch('ncurses-headers'),
        # http://bugs.python.org/issue29436
        LocalPatch('nl_langinfo'),
        LocalPatch('cppflags'),
        LocalPatch('ldflags-last'),
        LocalPatch('skip-build'),
        LocalPatch('ndk-issue399'),
        LocalPatch('android-force-sysmacros'),
    ]

    def __init__(self):
        super(Python, self).__init__()

        self.env['CONFIG_SITE'] = self.filesdir / 'config.site'

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
        self.run(['make', 'altinstall', f'DESTDIR={self.DESTDIR}'])
