#!/usr/bin/env bash
source ./env
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" ]] && (mkdir "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}/include" || exit 1)

TOOL_PREFIX=${ANDROID_NDK}/toolchains/${ANDROID_TOOLCHAIN}/prebuilt/linux-x86_64
CLANG_PREFIX=${ANDROID_NDK}/toolchains/llvm/prebuilt/linux-x86_64
export PREFIX="${ANDROID_PREFIX}/${BUILD_IDENTIFIER}"
export HOST="${ANDROID_HOST}"
export TARGET="${ANDROID_TARGET}"

export SDK_ROOT="${BASE}/sdk/${SDK_REL}"
export SDK_PLATFORM="android-${SDK_REV}"
export cross="${ANDROID_TARGET}-"

SYSROOT="${ANDROID_NDK}/platforms/android-${ANDROID_API_LEVEL}/arch-${ANDROID_PLATFORM}/usr"
LLVM_BASE_FLAGS="-target ${LLVM_TARGET} -gcc-toolchain ${TOOL_PREFIX} --sysroot ${SYSROOT}"

export CPPFLAGS="-I${PREFIX}/include -DANDROID ${CPPFLAGS_EXTRA}"
export CFLAGS="-Werror=implicit-function-declaration"
if [ "$ANDROID_API_LEVEL" -ge 21 ] ; then
    export CFLAGS="$CFLAGS -fPIE"
fi
export CFLAGS="${CFLAGS} ${CPPFLAGS_EXTRA}"
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="-L${PREFIX}/lib ${LDFLAGS_EXTRA}"

CLANG_BIN="${BASE}/clang-bin"
rm -rvf "${CLANG_BIN}"
mkdir "${CLANG_BIN}"
cat > "${CLANG_BIN}/cc" << EOF
#!/bin/bash
${CLANG_PREFIX}/bin/clang ${LLVM_BASE_FLAGS} "\$@"
EOF
cat > "${CLANG_BIN}/c++" << EOF
#!/bin/bash
${CLANG_PREFIX}/bin/clang++ ${LLVM_BASE_FLAGS} "\$@"
EOF
cat > "${CLANG_BIN}/cpp" << EOF
#!/bin/bash
${CLANG_PREFIX}/bin/clang -E ${LLVM_BASE_FLAGS} "\$@"
EOF

export CC="${CLANG_BIN}/cc"
export CXX="${CLANG_BIN}/c++"
export CPP="${CLANG_BIN}/cpp"
chmod +x "${CC}" "${CXX}" "${CPP}"

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

export PKG_CONFIG_LIBDIR="${PREFIX}/lib/pkgconfig"

pushd "${BASE}" > /dev/null
. "${FILESDIR}/build.sh" || exit 1
popd > /dev/null
