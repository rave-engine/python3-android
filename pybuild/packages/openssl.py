from ..builder import Builder
from ..package import Package
from ..patch import LocalPatch, RemotePatch
from ..source import GitSource, URLSource


openssl = Package('openssl')
main_repo = GitSource(openssl, 'https://github.com/openssl/openssl')
openssl.sources = [
    main_repo,
    URLSource(openssl, 'https://github.com/openssl/openssl/pull/2136.patch'),
]
openssl.patches = [
    LocalPatch(main_repo, 'fix-cflags'),
    LocalPatch(main_repo, 'destdir'),
    RemotePatch(main_repo, '2136'),
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
