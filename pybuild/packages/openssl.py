import logging
import os

from ..package import BasePackage
from ..patch import LocalPatch
from ..source import CPythonSourceDeps
from ..util import android_api_level, target_arch

logger = logging.getLogger(__name__)


class OpenSSL(BasePackage):
    patches = [
        LocalPatch('use-lld'),
        LocalPatch('lld-issue32518'),
    ]

    @property
    def source(self):
        return CPythonSourceDeps(branch='openssl-1.1.1')

    def init_build_env(self):
        from ..ndk import ndk

        super().init_build_env()

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

        self.env.update({
            'PATH': path,
            'HASHBANGPERL': '/system/bin/env perl',
        })
        self.env['CPPFLAGS'].append(f'-D__ANDROID_API__={android_api_level()}')

    def prepare(self):
        openssl_target = 'android-' + self.arch

        self.run_with_env(['perl', './Configure', '--prefix=/usr', '--openssldir=/etc/ssl', openssl_target, 'no-shared'])

    def build(self):
        self.run_with_env(['make'])
        self.run_with_env(['make', 'install_sw', 'install_ssldirs', f'DESTDIR={self.destdir()}'])
