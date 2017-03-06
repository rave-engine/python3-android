from ..builder import Builder
from ..source import GitSource
from ..package import Package
from ..util import target_arch

ncurses = Package('ncurses')
main_repo = GitSource(ncurses, 'https://github.com/ThomasDickey/ncurses-snapshots')
main_repo.alias = 'ncurses'
ncurses.sources = [main_repo]


class NCursesBuilder(Builder):
    source = main_repo

    def prepare(self):
        self.run_with_env([
            './configure',
            f'--host={target_arch().ANDROID_TARGET}',
            '--without-ada',
            '--without-manpages',
            '--without-progs',
            '--without-tests',
            '--without-termlib',
            '--enable-termcap',
            '--enable-widec',
            '--without-shared',
            '--with-normal',
            '--without-debug',
            '--without-cxx-binding',
            '--without-curses-h',
            '--with-warnings',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.DESTDIR}'])


ncurses.builder = NCursesBuilder()
