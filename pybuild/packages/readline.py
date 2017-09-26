from ..source import URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch


class Readline(Package):
    _MAJOR = 7
    _MINOR = 0
    _PATCHLEVEL = 3
    version = f'{_MAJOR}.{_MINOR}.{_PATCHLEVEL:03d}'

    _common = f'https://ftp.gnu.org/gnu/readline/readline-{_MAJOR}.{_MINOR}'
    source = URLSource(f'{_common}.tar.gz')
    dependencies = ['ncurses']

    # Use property as list comprehension creates a new scope not mixing with
    # the class scope
    _patches = None

    @property
    def patches(self):
        if self._patches is None:
            self._patches = [
                RemotePatch(
                    f'{self._common}-patches/readline{self._MAJOR}{self._MINOR}-{patch:03d}',
                    strip=0)
                for patch in range(1, self._PATCHLEVEL + 1)]
        return self._patches

    def prepare(self):
        # See the wcwidth() test in aclocal.m4. Tested on Android 6.0 and it's broken
        # XXX: wcwidth() is implemented in [1], which may be in Android P
        # Need a conditional configuration then?
        # [1] https://android.googlesource.com/platform/bionic/+/c41b560f5f624cbf40febd0a3ec0b2a3f74b8e42
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
