class Arch:
    ANDROID_TARGET: str

    @property
    def binutils_prefix(self):
        return self.ANDROID_TARGET


class arm(Arch):
    ANDROID_TARGET = 'armv7a-linux-androideabi'

    @property
    def binutils_prefix(self):
        return 'arm-linux-androideabi'


class arm64(Arch):
    ANDROID_TARGET = 'aarch64-linux-android'


class x86(Arch):
    ANDROID_TARGET = 'i686-linux-android'


class x86_64(Arch):
    ANDROID_TARGET = 'x86_64-linux-android'
