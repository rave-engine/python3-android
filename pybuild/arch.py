class Arch:
    ANDROID_TARGET: str

    @property
    def binutils_prefix(self):
        return self.ANDROID_TARGET


class arm(Arch):
    ANDROID_TARGET = 'armv7a-linux-androideabi'
    CMAKE_ANDROID_ABI = 'armeabi-v7a'

    @property
    def binutils_prefix(self):
        return 'arm-linux-androideabi'


class arm64(Arch):
    ANDROID_TARGET = 'aarch64-linux-android'
    CMAKE_ANDROID_ABI = 'arm64-v8a'


class x86(Arch):
    ANDROID_TARGET = 'i686-linux-android'
    CMAKE_ANDROID_ABI = 'x86'


class x86_64(Arch):
    ANDROID_TARGET = 'x86_64-linux-android'
    CMAKE_ANDROID_ABI = 'x86_64'
