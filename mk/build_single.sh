#!/usr/bin/env bash
source ./env
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" ]] && (mkdir "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" || exit 1)

export TOOL_PREFIX=${ANDROID_NDK}/toolchains/${ANDROID_TOOLCHAIN}/prebuilt/linux-x86_64
export CLANG_PREFIX=${ANDROID_NDK}/toolchains/llvm/prebuilt/linux-x86_64
export PREFIX="${ANDROID_PREFIX}/${BUILD_IDENTIFIER}"
export HOST="${ANDROID_HOST}"
export TARGET="${ANDROID_TARGET}"

export NDK_ROOT="${BASE}/sdk/${NDK_REL}"
export SDK_ROOT="${BASE}/sdk/${SDK_REL}"
export NDK_PLATFORM="android-${NDK_REV}"
export SDK_PLATFORM="android-${SDK_REV}"
export cross="${ANDROID_TARGET}-"

export SYSROOT="${ANDROID_NDK}/platforms/android-${ANDROID_API_LEVEL}/arch-${ANDROID_PLATFORM}/usr"
export LLVM_BASE_FLAGS="-target ${LLVM_TARGET} -gcc-toolchain ${TOOL_PREFIX}"

export CPPFLAGS="${LLVM_BASE_FLAGS} --sysroot ${SYSROOT} -I${PREFIX}/include -DANDROID ${CPPFLAGS_EXTRA}"
export CFLAGS="${LLVM_BASE_FLAGS} -Werror=implicit-function-declaration"
if [ "$ANDROID_API_LEVEL" -ge 21 ] ; then
    export CFLAGS="$CFLAGS -fPIE"
fi
export CFLAGS="${LLVM_BASE_FLAGS} ${CFLAGS} ${CPPFLAGS_EXTRA}"
export CXXFLAGS="${LLVM_BASE_FLAGS} ${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="${LLVM_BASE_FLAGS} --sysroot ${SYSROOT} -L${PREFIX}/lib ${LDFLAGS_EXTRA}"

export CC="${CLANG_PREFIX}/bin/clang"
export CXX="${CLANG_PREFIX}/bin/clang++"
export CPP="${CLANG_PREFIX}/bin/clang -E"
export AR="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ar"
export AS="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ls"
export LD="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ld"
export OBJCOPY="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-objcopy"
export OBJDUMP="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-objdump"
export RANLIB="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ranlib"
export STRIP="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-strip"
export READELF="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-readelf"

export NAME="$1"
export VERSION="$2"
export PACKAGE="${NAME}-${VERSION}"
export FILESDIR="${BASE}/mk/${NAME}"

pushd "${BASE}" > /dev/null
. "${FILESDIR}/build.sh" || exit 1
popd > /dev/null
