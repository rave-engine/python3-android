#!/usr/bin/env bash
source ./env
pushd "${BASE}" >/dev/null

prepare_ndk() {
   [[ ! -d "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)
   [[ ! -d "${BASE}/sdk/${NDK_REL}" ]] && (tar -xf "$BASE/sdk/android-ndk-r${NDK_REV}.tar.bz2" -C "$BASE/sdk" || exit 1)

   if [[ ! -f "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}" ]]; then
       ("${BASE}/sdk/${NDK_REL}/build/tools/make-standalone-toolchain.sh" --platform="android-${ANDROID_API_LEVEL}" --install-dir="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" --toolchain="${ANDROID_TOOLCHAIN}" && touch "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}") || exit 1
   fi
}

build() {
   what=$1
   version=$2

   if [[ ! -f "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}/${what}-${version}" ]]; then
       (/usr/bin/env bash --noprofile "${BASE}/_build_single.sh" "src/${what}-${version}.sh" && touch "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}/${what}-${version}") || exit 1
   fi
}


# Setup directories.
[[ ! -d "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_PREFIX}/${NDK_REV}-${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)

# Build stuff.
prepare_ndk
build bzip2   1.0.6
build xz      5.0.5
build openssl 1.0.0l
build Python  3.3.3

popd >/dev/null
