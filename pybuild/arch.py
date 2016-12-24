class Arch:
    ANDROID_COMPILER = '4.9'

    @property
    def ANDROID_TOOLCHAIN(self) -> str:
        return self.ANDROID_TOOLCHAIN_PREFIX + self.ANDROID_COMPILER


class arm(Arch):
    ANDROID_TARGET = 'arm-linux-androideabi'
    LLVM_TARGET = 'armv7-none-linux-androideabi'
    ANDROID_TOOLCHAIN_PREFIX = 'arm-linux-androideabi-'


class arm64(Arch):
    ANDROID_TARGET = 'aarch64-linux-android'
    LLVM_TARGET = 'aarch64-none-linux-android'
    ANDROID_TOOLCHAIN_PREFIX = 'aarch64-linux-android-'


class mips(Arch):
    ANDROID_TARGET = 'mipsel-linux-android'
    LLVM_TARGET = 'mipsel-none-linux-android'
    ANDROID_TOOLCHAIN_PREFIX = 'mipsel-linux-android-'


class mips64(Arch):
    ANDROID_TARGET = 'mips64el-linux-android'
    LLVM_TARGET = 'mips64el-none-linux-android'
    ANDROID_TOOLCHAIN_PREFIX = 'mips64el-linux-android-'


class x86(Arch):
    ANDROID_TARGET = 'i686-linux-android'
    LLVM_TARGET = 'i686-none-linux-android'
    ANDROID_TOOLCHAIN_PREFIX = 'x86-'


class x86_64(Arch):
    ANDROID_TARGET = 'x86_64-linux-android'
    LLVM_TARGET = 'x86_64-none-linux-android'
    ANDROID_TOOLCHAIN_PREFIX = 'x86_64-'
