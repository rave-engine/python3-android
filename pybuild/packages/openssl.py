import logging

from ..package import Package
from ..patch import LocalPatch
from ..source import URLSource

logger = logging.getLogger(__name__)


class OpenSSL(Package):
    version = '1.1.1a'
    source = URLSource(f'https://www.openssl.org/source/openssl-{version}.tar.gz', sig_suffix='.asc')
    patches = [
        LocalPatch('android'),
        LocalPatch('use-lld'),
        LocalPatch('lld-issue32518'),
    ]
    validpgpkeys = [
        '8657ABB260F056B1E5190839D9C4D26D0E604491',  # Matt Caswell
        '7953AC1FBC3DC8B3B292393ED5E9E43F7DF9EE8C',  # Richard Levitte
    ]

    def init_build_env(self) -> bool:
        if not super().init_build_env():
            return False

        self.env['HASHBANGPERL'] = '/system/bin/env perl'

        return True

    def prepare(self):
        openssl_target = 'android-' + self.arch

        self.run_with_env(['./Configure', '--prefix=/usr', '--openssldir=/etc/ssl', openssl_target, 'no-shared'])

    def build(self):
        self.run_with_env(['make'])
        self.run_with_env(['make', 'install_sw', 'install_ssldirs', f'DESTDIR={self.destdir()}'])
