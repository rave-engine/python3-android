import re

from ..source import URLSource
from ..package import Package
from ..patch import RemotePatch
from ..util import target_arch


class Readline(Package):
    validpgpkeys = ['7C0135FB088AAF6C66C650B9BB5869F064EA74AB']
    dependencies = ['ncurses']

    # Use property as list comprehension creates a new scope not mixing with
    # the class scope
    _patches = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mobj = re.match('(\d).(\d).(\d+)', self.version)
        self._major, self._minor, self._patchlevel = mobj.groups()

    def _common_url(self):
        return f'https://ftp.gnu.org/gnu/readline/readline-{self._major}.{self._minor}'

    @property
    def source(self):
        return URLSource(self._common_url() + '.tar.gz', sig_suffix='.sig')

    @property
    def patches(self):
        if self._patches is None:
            self._patches = [
                RemotePatch(
                    self._common_url() + f'-patches/readline{self._major}{self._minor}-{patch}',
                    strip=0, sig_suffix='.sig')
                for patch in range(1, int(self._patchlevel) + 1)]
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
