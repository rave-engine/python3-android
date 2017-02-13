from ..builder import Builder
from ..source import GitSource, URLSource
from ..package import Package
from ..patch import LocalPatch, RemotePatch
from ..util import target_arch

python = Package('python')
main_source = GitSource(python, 'https://github.com/python/cpython/')
python.sources = [
    main_source,
    # http://bugs.python.org/issue29436
    URLSource(python, 'http://bugs.python.org/file46503/nl_langinfo.patch'),
    # http://bugs.python.org/issue29440
    URLSource(python, 'http://bugs.python.org/file46517/gdbm.patch'),
]
python.patches = [
    RemotePatch(main_source, 'gdbm'),
    LocalPatch(main_source, 'ncurses-headers'),
    RemotePatch(main_source, 'nl_langinfo'),
    LocalPatch(main_source, 'remove-env-hack'),
    LocalPatch(main_source, 'ldflags-last'),
]


class PythonBuilder(Builder):
    source = main_source

    def __init__(self):
        super(PythonBuilder, self).__init__()

        self.env['CONFIG_SITE'] = python.filesdir / 'config.site'

    def prepare(self):
        self.run(['autoreconf', '--install', '--verbose', '--force'])

        self.run([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            # CPython requires explicit --build
            '--build=x86_64-linux-gnu',
            '--disable-ipv6',
            '--with-system-ffi',
            '--without-ensurepip',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'altinstall'])


python.builder = PythonBuilder()
