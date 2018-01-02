#!/usr/bin/env bash
source ./env
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" ]] && (mkdir "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" || exit 1)

export PATH="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}/bin:${PATH}"
export PREFIX="${ANDROID_PREFIX}/${BUILD_IDENTIFIER}"
export TOOL_PREFIX="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}"
export HOST="${ANDROID_HOST}"
export TARGET="${ANDROID_TARGET}"

export NDK_ROOT="${BASE}/sdk/${NDK_REL}"
export SDK_ROOT="${BASE}/sdk/${SDK_REL}"
export NDK_PLATFORM="android-${NDK_REV}"
export SDK_PLATFORM="android-${SDK_REV}"
export cross="${ANDROID_TARGET}-"

# BDS NEW
CLANG_PREFIX="${NDK_ROOT}/toolchains/llvm/prebuilt/linux-x86_64"
export SYSROOT="${BASE}/build-tools/${BUILD_IDENTIFIER}" 
##SYSROOT_INCLUDE="${NDK_ROOT}/sysroot"



case "${NDK_REV}" in
  16*)
	   export NDK_SYS_ROOT="${NDK_ROOT}/sysroot"
	   ;;
	*)
	   export NDK_SYS_ROOT="${TOOL_PREFIX}/sysroot"
	   ;;
esac	   

export NEW_SYSROOT="${NDK_ROOT}/platforms/android-${ANDROID_API_LEVEL}/arch-x86_64/usr"


# case "${NDK_REV}" in
#   15*|16*)
#       #export CFLAGS="--sysroot ${NDK_SYS_ROOT} -I${TOOL_PREFIX}/include -DANDROID -mandroid ${CFLAGS_EXTRA} -isystem ${TOOL_PREFIX}/sysroot/usr/include/${ANDROID_TARGET} -D__ANDROID_API__=${ANDROID_API_LEVEL}" 
#       export CFLAGS="--sysroot ${NDK_SYS_ROOT} -I${TOOL_PREFIX}/include -DANDROID ${CFLAGS_EXTRA} -isystem ${TOOL_PREFIX}/sysroot/usr/include/${ANDROID_TARGET} -D__ANDROID_API__=${ANDROID_API_LEVEL}" 
#       ;;
#   *)
# 	  export CFLAGS="--sysroot ${TOOL_PREFIX}/sysroot -I${PREFIX}/include -I${TOOL_PREFIX}/include -DANDROID -mandroid ${CFLAGS_EXTRA}" 
#       ;;
# esac


export LLVM_BASE_FLAGS="-target ${LLVM_TARGET} -gcc-toolchain ${TOOL_PREFIX}"


##export CPPFLAGS="${LLVM_BASE_FLAGS} --sysroot ${NEW_SYSROOT} -I${SYSROOT_INCLUDE}/usr/include/${ANDROID_TARGET} -I${PREFIX}/include -DANDROID ${CPPFLAGS_EXTRA}"
export CPPFLAGS="${LLVM_BASE_FLAGS} --sysroot ${NEW_SYSROOT} -I${NEW_SYSROOT}/include -I${PREFIX}/include -DANDROID ${CPPFLAGS_EXTRA} -D__ANDROID_API__=${ANDROID_API_LEVEL}"
#export CXXFLAGS="--sysroot ${SYSROOT}"
##export CFLAGS="${LLVM_BASE_FLAGS} -I${SYSROOT_INCLUDE}/usr/include -I${SYSROOT_INCLUDE}/usr/include/${ANDROID_TARGET} -D__ANDROID_API__=${ANDROID_API_LEVEL} -Werror=implicit-function-declaration"
export CFLAGS="${LLVM_BASE_FLAGS}  -I${NEW_SYSROOT}/include -Werror=implicit-function-declaration"
if [ "$ANDROID_API_LEVEL" -ge 21 ] ; then	
    export CFLAGS="$CFLAGS -fPIE"
fi
export CFLAGS="${CFLAGS} ${CPPFLAGS_EXTRA}"
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="${LLVM_BASE_FLAGS} --sysroot ${NEW_SYSROOT} -L${PREFIX}/lib ${LDFLAGS_EXTRA}"
#export LDFLAGS="-L${PREFIX}/lib ${LDFLAGS_EXTRA}"

echo "SYSROOT_INCLUDE IS ${NEW_SYSROOT}"
#echo "Hello World LDFlags=${LDFLAGS}" 

# export CPPFLAGS="${CFLAGS} ${CPPFLAGS_EXTRA}"
# export CXXFLAGS="${CFLAGS} ${CXXFLAGS_EXTRA}"
# export LDFLAGS="--sysroot ${TOOL_PREFIX}/sysroot -L${PREFIX}/lib -L${TOOL_PREFIX}/lib ${LDFLAGS_EXTRA}"

# export CC="${ANDROID_TARGET}-gcc"
# export CXX="${ANDROID_TARGET}-g++"
# export CPP="${ANDROID_TARGET}-cpp"
export CC="${CLANG_PREFIX}/bin/cc"
export CXX="${CLANG_PREFIX}/bin/c++"
export CPP="${CLANG_PREFIX}/bin/cpp"

chmod +x "${CC}" "${CXX}" "${CPP}"


export AR="${ANDROID_TARGET}-ar"
export AS="${ANDROID_TARGET}-ls"
export LD="${ANDROID_TARGET}-ld"
export OBJCOPY="${ANDROID_TARGET}-objcopy"
export OBJDUMP="${ANDROID_TARGET}-objdump"
export RANLIB="${ANDROID_TARGET}-ranlib"
export STRIP="${ANDROID_TARGET}-strip"

export NAME="$1"
export VERSION="$2"
export PACKAGE="${NAME}-${VERSION}"
export FILESDIR="${BASE}/mk/${NAME}/${VERSION}"

pushd "${BASE}" > /dev/null
. "${FILESDIR}/build.sh" || exit 1
popd > /dev/null
