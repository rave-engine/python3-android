from ..builder import Builder
from ..source import MercurialSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch

python = Package('python')
main_source = MercurialSource(python, 'https://hg.python.org/cpython/')
python.sources = [main_source]
python.patches = [
    LocalPatch(main_source, 'check-crypt'),
    LocalPatch(main_source, 'gdbm'),
    LocalPatch(main_source, 'decimal'),
    LocalPatch(main_source, 'ncurses-headers'),
    LocalPatch(main_source, 'distutils-android-sysroot'),
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
