from ..builder import Builder
from ..source import GitSource, URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch

libffi = Package('libffi')
main_repo = GitSource(libffi, 'https://github.com/libffi/libffi')
libffi.sources = [
    main_repo,
    URLSource(libffi, 'https://github.com/libffi/libffi/pull/265.patch'),
]
libffi.patches = [
    RemotePatch(main_repo, '265'),
]


class LibFFIBuilder(Builder):
    source = main_repo

    def prepare(self):
        self.run(['./autogen.sh'])

        self.run_with_env([
            './configure',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.DESTDIR}'])


libffi.builder = LibFFIBuilder()
