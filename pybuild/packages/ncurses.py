import re

from ..source import GitSource
from ..package import Package
from ..util import target_arch


class NCursesSource(GitSource):
    def __init__(self):
        super().__init__('https://github.com/ThomasDickey/ncurses-snapshots')

    def get_version(self):
        return re.sub(r'v(\d+)_(\d+)_(\d+)', r'\1.\2-\3', super().get_version())


class NCurses(Package):
    source = NCursesSource()

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
