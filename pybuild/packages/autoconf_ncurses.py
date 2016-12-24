from ..builder import Builder
from ..source import URLSource
from ..package import Package

autoconf_ncurses = Package('autoconf_ncurses')
main_source = URLSource(autoconf_ncurses, 'http://invisible-mirror.net/archives/autoconf/autoconf-2.52-20150926.tgz')
autoconf_ncurses.sources = [main_source]


class AutoconfNCursesBuilder(Builder):
    source = main_source

    def prepare(self):
        self.run([
            './configure',
            '--prefix=' + str(self.BUILDDIR / 'host' / 'usr')
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', 'DESTDIR='])


autoconf_ncurses.builder = AutoconfNCursesBuilder()
