from ..builder import Builder
from ..package import Package
from ..patch import LocalPatch
from ..source import GitSource


openssl = Package('openssl')
main_repo = GitSource(openssl, 'https://github.com/openssl/openssl')
openssl.sources = [main_repo]
openssl.patches = [
    LocalPatch(main_repo, 'fix-cflags'),
    LocalPatch(main_repo, 'destdir'),
]


class OpenSSLBuilder(Builder):
    OPENSSL_TARGETS = {
        'arm': 'android-armeabi',
        'arm64': 'android64-aarch64',
        'x86': 'android-x86',
        'x86_64': 'android64-x86_64',
        'mips': 'android-mips',
        'mips64': 'android64-mips64',
    }

    source = main_repo

    def prepare(self):
        openssl_target = self.OPENSSL_TARGETS[self.ANDROID_PLATFORM]

        self.run(['./Configure', '--prefix=/usr', '--openssldir=/etc/ssl', openssl_target, 'no-shared'])

    def build(self):
        self.run(['make'])
        self.run(['make', 'install_sw', 'install_ssldirs'])


openssl.builder = OpenSSLBuilder()
