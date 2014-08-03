source ./env

export PATH="${ANDROID_TOOL_PREFIX}/bin:${PATH}"
export PREFIX="${ANDROID_PREFIX}/${NDK_REV}-${ANDROID_PLATFORM}"
export TOOL_PREFIX="${ANDROID_TOOL_PREFIX}"
export HOST="${ANDROID_HOST}"
export TARGET="${ANDROID_TARGET}"

export NDK_ROOT="$(dirname "$0")/sdk/${NDK_REL}"
export SDK_ROOT="$(dirname "$0")/sdk/${SDK_REL}"
export NDK_PLATFORM="android-${NDK_REV}"
export SDK_PLATFORM="android-${SDK_REV}"
export cross="${ANDROID_TARGET}-"

export CFLAGS="--sysroot ${TOOL_PREFIX}/sysroot -I${PREFIX}/include -I${TOOL_PREFIX}/include -DANDROID -mandroid ${CFLAGS_EXTRA}"
export CPPFLAGS="${CFLAGS} ${CPPFLAGS_EXTRA}"
export CXXFLAGS="${CFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="--sysroot ${TOOL_PREFIX}/sysroot -L${PREFIX}/lib -L${TOOL_PREFIX}/lib ${LDFLAGS_EXTRA}"

export CC="${ANDROID_TARGET}-gcc"
export CXX="${ANDROID_TARGET}-g++"
export CPP="${ANDROID_TARGET}-cpp"
export AR="${ANDROID_TARGET}-ar"
export AS="${ANDROID_TARGET}-ls"
export LD="${ANDROID_TARGET}-ld"
export OBJCOPY="${ANDROID_TARGET}-objcopy"
export OBJDUMP="${ANDROID_TARGET}-objdump"
export RANLIB="${ANDROID_TARGET}-ranlib"
export STRIP="${ANDROID_TARGET}-strip"

. "${BASE}/$1"
