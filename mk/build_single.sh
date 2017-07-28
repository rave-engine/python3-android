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


case "${NDK_REV}" in
  15*)
      export CFLAGS="--sysroot ${TOOL_PREFIX}/sysroot -I${TOOL_PREFIX}/include -DANDROID -mandroid ${CFLAGS_EXTRA} -isystem ${TOOL_PREFIX}/sysroot/usr/include/${ANDROID_TARGET} -D__ANDROID_API__=${ANDROID_API_LEVEL}" 
      ;;
  *)
	  export CFLAGS="--sysroot ${TOOL_PREFIX}/sysroot -I${PREFIX}/include -I${TOOL_PREFIX}/include -DANDROID -mandroid ${CFLAGS_EXTRA}" 
      ;;
esac

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

export NAME="$1"
export VERSION="$2"
export PACKAGE="${NAME}-${VERSION}"
export FILESDIR="${BASE}/mk/${NAME}/${VERSION}"

pushd "${BASE}" > /dev/null
. "${FILESDIR}/build.sh" || exit 1
popd > /dev/null
