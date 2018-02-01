from ..source import GitSource
from ..package import Package
from ..util import target_arch


class NCurses(Package):
    source = GitSource('https://github.com/ThomasDickey/ncurses-snapshots', alias='ncurses')

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
