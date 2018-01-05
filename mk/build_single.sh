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

export TOOL_PREFIX="${NDK_ROOT}/toolchains/${ANDROID_TOOLCHAIN}/prebuilt/linux-x86_64"
export CLANG_PREFIX="${NDK_ROOT}/toolchains/llvm/prebuilt/linux-x86_64"
export LLVM_BASE_FLAGS="-target ${LLVM_TARGET} -gcc-toolchain ${TOOL_PREFIX}"
export ARCH_SYSROOT="${NDK_ROOT}/platforms/android-${ANDROID_API_LEVEL}/arch-${ANDROID_PLATFORM}/usr"
export UNIFIED_SYSROOT="${NDK_ROOT}/sysroot/usr"

export CC="${CLANG_PREFIX}/bin/clang"
export CXX="${CLANG_PREFIX}/bin/clang++"
export CPP="${CLANG_PREFIX}/bin/clang"

export CPPFLAGS="${LLVM_BASE_FLAGS} --sysroot=${ARCH_SYSROOT} -isystem ${UNIFIED_SYSROOT}/include -isystem ${UNIFIED_SYSROOT}/include/${ANDROID_TARGET} -D__ANDROID_API__=${ANDROID_API_LEVEL}"

export CFLAGS="-fPIC"

case "${ANDROID_PLATFORM}" in
  arm)
      export CFLAGS="${CFLAGS} -fno-integrated-as" 
      ;;
esac


export CXXFLAGS="${CFLAGS}"
export LDFLAGS="${LLVM_BASE_FLAGS} --sysroot=${ARCH_SYSROOT} -pie"


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


chmod +x "${CC}" "${CXX}" "${CPP}"
#chmod -R +x * "${NDK_ROOT}"


export NAME="$1"
export VERSION="$2"
export PACKAGE="${NAME}-${VERSION}"
export FILESDIR="${BASE}/mk/${NAME}/${VERSION}"

pushd "${BASE}" > /dev/null
. "${FILESDIR}/build.sh" || exit 1
popd > /dev/null
