#!/usr/bin/env bash
set -e

source ./env
source "${BASE}/mk/common.sh"

[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" ]] && mkdir -p "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}"

UNAME=$(uname -s)
case $UNAME in
    Linux)
        HOST_OS=linux
        ;;
    Darwin)
        HOST_OS=darwin
        ;;
    *)
        echo "Unsupported system $UNAME"
        exit 1
esac

TOOL_PREFIX=${ANDROID_NDK}/toolchains/${ANDROID_TOOLCHAIN}/prebuilt/${HOST_OS}-x86_64
CLANG_PREFIX=${ANDROID_NDK}/toolchains/llvm/prebuilt/${HOST_OS}-x86_64
export DESTDIR="${ANDROID_PREFIX}/${BUILD_IDENTIFIER}"
export HOST="${ANDROID_HOST}"
export TARGET="${ANDROID_TARGET}"

SYSROOT="${ANDROID_NDK}/platforms/android-${ANDROID_API_LEVEL}/arch-${ANDROID_PLATFORM}/usr"
LLVM_BASE_FLAGS="-target ${LLVM_TARGET} -gcc-toolchain ${TOOL_PREFIX} --sysroot=${SYSROOT}"

export CPPFLAGS="-I${DESTDIR}/usr/include"
export CFLAGS="-fPIE"
export CXXFLAGS="-fPIE"
export LDFLAGS="-pie -L${DESTDIR}/usr/lib"

# OpenSSL doesn't work without -fno-integrated-as
# TODO: figure out flags for other architectures
case "$ANDROID_PLATFORM" in
    arm64)  export CFLAGS="$CFLAGS -fno-integrated-as";;
    arm)    export CFLAGS="$CFLAGS -fno-integrated-as";;
    mips)   export CFLAGS="$CFLAGS -fno-integrated-as";;
    mips64) export CFLAGS="$CFLAGS -fno-integrated-as";;
esac

export CC="${CLANG_PREFIX}/bin/clang ${LLVM_BASE_FLAGS}"
export CXX="${CLANG_PREFIX}/bin/clang++ ${LLVM_BASE_FLAGS}"
export CPP="${CLANG_PREFIX}/bin/clang -E ${LLVM_BASE_FLAGS}"
export AR="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ar"
export AS="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-as"
export LD="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ld --sysroot=${SYSROOT}"
export OBJCOPY="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-objcopy"
export OBJDUMP="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-objdump"
export RANLIB="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ranlib"
export STRIP="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-strip"
export READELF="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-readelf"

export NAME="$1"
export FILESDIR="${BASE}/mk/${NAME}"

export PKG_CONFIG_LIBDIR="${DESTDIR}/usr/lib/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="${DESTDIR}"

if [ -z "$SKIP_CLEAN" ] ; then
    clean_and_extract_package $NAME
fi

pushd "${BASE}/src/$(get_source_folder $NAME)"
if [ -z "$SKIP_CLEAN" -a -f "${FILESDIR}/prepare.sh" ] ; then
    bash --norc --noprofile -e "${FILESDIR}/prepare.sh"
fi
bash --norc --noprofile -e "${FILESDIR}/build.sh"
popd
