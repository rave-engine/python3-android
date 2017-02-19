from ..builder import Builder
from ..package import Package
from ..patch import LocalPatch
from ..source import GitSource


openssl = Package('openssl')
main_repo = GitSource(openssl, 'https://github.com/openssl/openssl')
openssl.sources = [
    main_repo,
]
openssl.patches = [
    LocalPatch(main_repo, 'ndk-clang-targets'),
    LocalPatch(main_repo, 'sh'),
]


class OpenSSLBuilder(Builder):
    OPENSSL_TARGETS = {
        'arm': 'android-armeabi-clang',
        'arm64': 'android64-aarch64-clang',
        'x86': 'android-x86-clang',
        'x86_64': 'android64-x86_64-clang',
        'mips': 'android-mips-clang',
        'mips64': 'android64-mips64-clang',
    }

    source = main_repo

    def __init__(self):
        super(OpenSSLBuilder, self).__init__()

        self.env['HASHBANGPERL'] = '/system/bin/env perl'
        self.env['HASHBANGSH'] = '/system/bin/sh'

    def prepare(self):
        openssl_target = self.OPENSSL_TARGETS[self.ANDROID_PLATFORM]

        self.run_with_env(['./Configure', '--prefix=/usr', '--openssldir=/etc/ssl', openssl_target, 'no-shared'])

    def build(self):
        configure_env = self.env
        self.env = {}
        for key in ('ARCH_SYSROOT', 'ANDROID_API_LEVEL'):
            self.env[key] = configure_env[key]
        self.env.update({
            'CROSS_SYSROOT': configure_env['UNIFIED_SYSROOT'],
            'GCC_TOOLCHAIN': self.TOOL_PREFIX,
        })
        self.run_with_env(['make'])
        self.run_with_env(['make', 'install_sw', 'install_ssldirs', f'DESTDIR={self.DESTDIR}'])


openssl.builder = OpenSSLBuilder()
