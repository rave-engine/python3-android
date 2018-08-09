from ..patch import LocalPatch
from ..source import URLSource
from ..package import Package


class BZip2(Package):
    version = '1.0.6'
    source = URLSource(f'https://fossies.org/linux/misc/bzip2-{version}.tar.gz')
    patches = [
        LocalPatch('makefiles'),
    ]

    def init_build_env(self) -> bool:
        if not super().init_build_env():
            return False

        self.env['CFLAGS'] = self.env['CPPFLAGS'] + self.env['CFLAGS']

        return True

    def build(self):
        self.run_with_env(['make', 'libbz2.a', 'bzip2', 'bzip2recover'])
        self.run_with_env(['make', 'install', f'PREFIX={self.destdir()}/usr'])
