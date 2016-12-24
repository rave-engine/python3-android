from ..builder import Builder
from ..source import GitSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch

readline = Package('readline')
main_repo = GitSource(readline, 'http://git.savannah.gnu.org/r/readline.git')
readline.sources = [main_repo]
readline.patches = [
    LocalPatch(main_repo, 'destdir'),
]


class ReadlineBuilder(Builder):
    source = main_repo

    def prepare(self):
        # See the wcwidth() test in aclocal.m4. Tested on Android 6.0 and it's broken
        self.run([
            './configure',
            'bash_cv_wcwidth_broken=yes',
            '--prefix=/usr',
            '--host=' + target_arch().ANDROID_TARGET,
            '--disable-shared',
        ])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install'])


readline.builder = ReadlineBuilder()
