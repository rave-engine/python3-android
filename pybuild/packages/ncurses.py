from ..source import URLSource
from ..package import Package
from ..util import target_arch


class NCurses(Package):
    version = '6.1-20180908'
    source = URLSource(f'https://invisible-mirror.net/archives/ncurses/current/ncurses-{version}.tgz', sig_suffix='.asc')
    validpgpkeys = ['C52048C0C0748FEE227D47A2702353E0F7E48EDB']

    def prepare(self):
        self.run_with_env([
            './configure',
            '--prefix=/usr',
            f'--host={target_arch().ANDROID_TARGET}',
            '--without-ada',
            '--enable-widec',
            '--without-shared',
            '--with-normal',
            '--without-debug',
            '--without-cxx-binding',
            '--enable-warnings',
            '--disable-stripping',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
