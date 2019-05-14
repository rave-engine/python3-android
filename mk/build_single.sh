#!/usr/bin/env bash
source ./env
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" ]] && (mkdir "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" || exit 1)


#export PATH="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}/bin:${PATH}"
export PREFIX="${ANDROID_PREFIX}/${BUILD_IDENTIFIER}"
export TOOL_PREFIX="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}"
export HOST="${ANDROID_HOST}"
export TARGET="${ANDROID_TARGET}"

export NDK_ROOT="${BASE}/sdk/${NDK_REL}"

# This should give us darwin or linux
export BUILD_OS="$(uname | tr '[A-Z]' '[a-z'])"

export TOOL_PREFIX="${NDK_ROOT}/toolchains/llvm/prebuilt/${BUILD_OS}-x86_64"
export CLANG_PREFIX="${NDK_ROOT}/toolchains/llvm/prebuilt/${BUILD_OS}-x86_64"
export LLVM_BASE_FLAGS="-target ${LLVM_TARGET}"
export ARCH_SYSROOT="${NDK_ROOT}/platforms/android-${ANDROID_API_LEVEL}/arch-${ANDROID_PLATFORM}/usr"
export UNIFIED_SYSROOT="${NDK_ROOT}/sysroot/usr"


# SSH Needed?
export CROSS_SYSROOT="${UNIFIED_SYSROOT}"
export GCC_TOOLCHAIN="${TOOL_PREFIX}"



export CC="${CLANG_PREFIX}/bin/clang"
export CXX="${CLANG_PREFIX}/bin/clang++"
export CPP="${CC} -E"

chmod +x "${CC}" "${CXX}"

export CPPFLAGS="${LLVM_BASE_FLAGS}"

export CFLAGS="-fPIC"

## This doesn't seem to work, but did for other project
# case "${ANDROID_PLATFORM}" in
#   arm)
#       export CFLAGS="${CFLAGS} -fno-integrated-as" 
#       ;;
# esac


export CXXFLAGS="${CFLAGS}"
##export LDFLAGS="${LLVM_BASE_FLAGS} --sysroot=${ARCH_SYSROOT} -pie"
export LDFLAGS="${LLVM_BASE_FLAGS} -fuse-ld=lld"


#?????
# export CPPFLAGS="$CPPFLAGS -${CPPFLAGS_EXTRA}"
# export LDFLAGS="$LDFLAGS ${"


# self.env['CPPFLAGS'].extend(['-I', f'{dep_pkg.destdir()}/usr/include'])
# self.env['LDFLAGS'].extend(['-L', f'{dep_pkg.destdir()}/usr/lib'])



export AR="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ar"
export AS="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-as"
export LD="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ld"
export OBJCOPY="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-objcopy"
export OBJDUMP="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-objdump"
export RANLIB="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-ranlib"
export STRIP="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-strip"
export READELF="${TOOL_PREFIX}/bin/${ANDROID_TARGET}-readelf"

export PATH="${TOOL_PREFIX}/${ANDROID_TARGET}/bin:${PATH}"




export NAME="$1"
export VERSION="$2"
export PACKAGE="${NAME}-${VERSION}"
export FILESDIR="${BASE}/mk/${NAME}/${VERSION}"

pushd "${BASE}" > /dev/null
. "${FILESDIR}/build.sh" || exit 1
popd > /dev/null
