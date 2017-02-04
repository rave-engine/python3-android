from ..builder import Builder
from ..source import MercurialSource, URLSource
from ..package import Package
from ..patch import LocalPatch, RemotePatch
from ..util import target_arch

python = Package('python')
main_source = MercurialSource(python, 'https://hg.python.org/cpython/')
python.sources = [
    main_source,
    # http://bugs.python.org/issue27659
    URLSource(python, 'http://bugs.python.org/file46302/prohibit-implicit-function-declarations.patch'),
    # http://bugs.python.org/issue29436
    URLSource(python, 'http://bugs.python.org/file46503/nl_langinfo.patch'),
    # http://bugs.python.org/issue29439
    URLSource(python, 'http://bugs.python.org/file46506/decimal.patch'),
    # http://bugs.python.org/issue29440
    URLSource(python, 'http://bugs.python.org/file46507/gdbm.patch'),
]
python.patches = [
    RemotePatch(main_source, 'prohibit-implicit-function-declarations'),
    RemotePatch(main_source, 'gdbm'),
    RemotePatch(main_source, 'decimal'),
    LocalPatch(main_source, 'ncurses-headers'),
    RemotePatch(main_source, 'nl_langinfo'),
    # The order of three patches below is important!
    LocalPatch(main_source, 'setup-argparse'),
    LocalPatch(main_source, 'detect_macros'),
    LocalPatch(main_source, 'sysroot-flags'),
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
