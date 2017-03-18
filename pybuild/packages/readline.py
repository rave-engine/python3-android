from ..source import URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch


class Readline(Package):
    source = URLSource('ftp://ftp.cwru.edu/pub/bash/readline-7.0.tar.gz')
    extra_sources = [
        URLSource('ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-001'),
        URLSource('ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-002'),
        URLSource('ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-003'),
    ]
    patches = [
        RemotePatch('readline70-001', strip=0),
        RemotePatch('readline70-002', strip=0),
        RemotePatch('readline70-003', strip=0),
    ]

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
