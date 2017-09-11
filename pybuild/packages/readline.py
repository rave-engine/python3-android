from ..source import GitSource
from ..package import Package
from ..util import target_arch


class Readline(Package):
    source = GitSource('https://git.savannah.gnu.org/git/readline.git',
                       alias='readline', branch='devel')
    dependencies = ['ncurses']

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
        self.run(['make', 'install', f'DESTDIR={self.destdir()}'])
