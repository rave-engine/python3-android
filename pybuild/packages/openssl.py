import logging
import os

from ..ndk import ndk
from ..package import BasePackage
from ..patch import LocalPatch
from ..source import URLSource
from ..util import android_api_level, target_arch

logger = logging.getLogger(__name__)


class OpenSSL(BasePackage):
    version = '1.1.1c'
    source = URLSource(f'https://www.openssl.org/source/openssl-{version}.tar.gz', sig_suffix='.asc')
    patches = [
        LocalPatch('use-lld'),
        LocalPatch('lld-issue32518'),
    ]
    validpgpkeys = [
        '8657ABB260F056B1E5190839D9C4D26D0E604491',  # Matt Caswell
        '7953AC1FBC3DC8B3B292393ED5E9E43F7DF9EE8C',  # Richard Levitte
    ]

    def init_build_env(self):
        # OpenSSL handles NDK internal paths by itself, so don't use CC, CFLAGS, ...
        # from pybuild
        path = os.pathsep.join((
            # OpenSSL requires NDK's clang in $PATH to enable usage of clang
            str(ndk.unified_toolchain),
            # and it requires unprefixed binutils, too
            str(ndk.unified_toolchain.parent / target_arch().ANDROID_TARGET / 'bin'),
            os.environ['PATH'],
        ))

        logger.debug(f'$PATH for OpenSSL: {path}')

        self.env = {
            'PATH': path,
            'CPPFLAGS': f'-D__ANDROID_API__={android_api_level()}',
            'HASHBANGPERL': '/system/bin/env perl',
        }

    def prepare(self):
        openssl_target = 'android-' + self.arch

        self.run_with_env(['./Configure', '--prefix=/usr', '--openssldir=/etc/ssl', openssl_target, 'no-shared'])

    def build(self):
        self.run_with_env(['make'])
        self.run_with_env(['make', 'install_sw', 'install_ssldirs', f'DESTDIR={self.destdir()}'])
