#!/usr/bin/env bash
source ./env
pushd "${BASE}" >/dev/null

prepare_ndk() {
   [[ ! -d "${ANDROID_TOOL_PREFIX}" ]] && (mkdir "${ANDROID_TOOL_PREFIX}" || exit 1)
   [[ ! -d "${BASE}/sdk/${NDK_REL}" ]] && (tar -xf "$BASE/sdk/android-ndk-r${NDK_REV}.tar.bz2" -C "$BASE/sdk" || exit 1)

   if [[ ! -f "${ANDROID_PREFIX}/.built-ndk-${NDK_REV}" ]]; then
       ("${BASE}/sdk/${NDK_REL}/build/tools/make-standalone-toolchain.sh" --platform="android-${SDK_REV}" --install-dir="${ANDROID_TOOL_PREFIX}" --toolchain="${ANDROID_TOOLCHAIN}" && touch "${ANDROID_PREFIX}/.built-ndk-${NDK_REV}") || exit 1
   fi
}

build() {
   what=$1
   version=$2

   if [[ ! -f "${ANDROID_PREFIX}/.built-${NDK_REV}-${ANDROID_PLATFORM}/${what}-${version}" ]]; then
       (/usr/bin/env bash --noprofile "${BASE}/_build_single.sh" "src/${what}-${version}.sh" && touch "${ANDROID_PREFIX}/.built-${NDK_REV}-${ANDROID_PLATFORM}/${what}-${version}") || exit 1
   fi
}


# Setup directories.
[[ ! -d "${ANDROID_PREFIX}/.built-${NDK_REV}-${ANDROID_PLATFORM}" ]] && (mkdir -p "${ANDROID_PREFIX}/.built-${NDK_REV}-${ANDROID_PLATFORM}" || exit 1)
[[ ! -d "${ANDROID_PREFIX}/${NDK_REV}-${ANDROID_PLATFORM}" ]] && (mkdir -p "${ANDROID_PREFIX}/${NDK_REV}-${ANDROID_PLATFORM}" || exit 1)

# Build stuff.
prepare_ndk
build bzip2   1.0.6
build xz      5.0.5
build openssl 1.0.0l
build Python  3.3.3

popd >/dev/null
