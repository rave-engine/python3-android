from ..builder import Builder
from ..source import URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch

readline = Package('readline')
main_source = URLSource(readline, 'ftp://ftp.cwru.edu/pub/bash/readline-7.0.tar.gz')
readline.sources = [
    main_source,
    URLSource(readline, 'ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-001'),
    URLSource(readline, 'ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-002'),
    URLSource(readline, 'ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-003'),
]
readline.patches = [
    RemotePatch(main_source, 'readline70-001', strip=0),
    RemotePatch(main_source, 'readline70-002', strip=0),
    RemotePatch(main_source, 'readline70-003', strip=0),
]


class ReadlineBuilder(Builder):
    source = main_source

    def prepare(self):
        # See the wcwidth() test in aclocal.m4. Tested on Android 6.0 and it's broken
        self.run_with_env([
            './configure',
            'bash_cv_wcwidth_broken=yes',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install', f'DESTDIR={self.DESTDIR}'])


readline.builder = ReadlineBuilder()
