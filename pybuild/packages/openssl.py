import copy
import logging
import os

from ..package import Package
from ..source import URLSource
from ..util import android_api_level, target_arch

logger = logging.getLogger(__name__)


class OpenSSL(Package):
    version = '1.1.1'
    source = URLSource(f'https://www.openssl.org/source/openssl-{version}.tar.gz', sig_suffix='.asc')
    validpgpkeys = [
        '8657ABB260F056B1E5190839D9C4D26D0E604491',  # Matt Caswell
        '7953AC1FBC3DC8B3B292393ED5E9E43F7DF9EE8C',  # Richard Levitte
    ]

    def init_build_env(self) -> bool:
        if not super().init_build_env():
            return False

        # OpenSSL handles NDK internal paths by itself, so don't use CC, CFLAGS, ...
        # from pybuild
        old_env = copy.deepcopy(self.env)
        newpath = os.pathsep.join((
            # OpenSSL requires NDK's clang in $PATH to enable usage of clang
            os.path.dirname(old_env['CC']),
            # and it requires unprefixed binutils, too
            str(self.TOOL_PREFIX / target_arch().ANDROID_TARGET / 'bin'),
            os.environ['PATH'],
        ))

        logger.debug(f'$PATH for OpenSSL: {newpath}')

        self.env = {
            'PATH': newpath,
            'CPPFLAGS': f'-D__ANDROID_API__={android_api_level()}',
        }

        self.env['HASHBANGPERL'] = '/system/bin/env perl'

        return True

    def prepare(self):
        openssl_target = 'android-' + self.arch

        self.run_with_env(['./Configure', '--prefix=/usr', '--openssldir=/etc/ssl', openssl_target, 'no-shared'])

    def build(self):
        self.run_with_env(['make'])
        self.run_with_env(['make', 'install_sw', 'install_ssldirs', f'DESTDIR={self.destdir()}'])
