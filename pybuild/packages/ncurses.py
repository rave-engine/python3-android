import os

from ..builder import Builder
from ..patch import LocalPatch
from ..source import GitSource
from ..package import Package
from ..util import target_arch

ncurses = Package('ncurses')
main_repo = GitSource(ncurses, 'https://github.com/ThomasDickey/ncurses-snapshots')
main_repo.alias = 'ncurses'
ncurses.sources = [main_repo]
ncurses.patches = [
    LocalPatch(main_repo, 'skip-cc-env-check'),
]


class NCursesBuilder(Builder):
    source = main_repo

    def __init__(self):
        super(NCursesBuilder, self).__init__()
        # Use Thomas Dickey's patched autoconf
        self.env['PATH'] = f'{self.BUILDDIR}/host/usr/bin' + os.pathsep + os.getenv('PATH')

    def prepare(self):
        self.run(['autoreconf', '--install', '--verbose', '--force'])

        self.run([
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
        self.run(['make', 'install'])


ncurses.builder = NCursesBuilder()
