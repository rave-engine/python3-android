from ..source import URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch


class Readline(Package):
    source = URLSource('ftp://ftp.cwru.edu/pub/bash/readline-7.0.tar.gz')
    patches = [
        RemotePatch(f'ftp://ftp.cwru.edu/pub/bash/readline-7.0-patches/readline70-{i:03d}', strip=0)
        for i in range(1, 4)
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
