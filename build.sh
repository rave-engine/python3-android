#!/bin/bash
source ./env
pushd "${BASE}" >/dev/null

prepare_ndk() {
   [[ ! -d "${ANDROID_TOOL_PREFIX}" ]] && (mkdir "${ANDROID_TOOL_PREFIX}" || exit 1)
   if [[ ! -f "${BASE}/.built/_ndk" ]]; then
       ("${BASE}/sdk/${NDK_REL}/build/tools/make-standalone-toolchain.sh" --platform="android-${SDK_REV}" --install-dir="${ANDROID_TOOL_PREFIX}" --toolchain="${ANDROID_TOOLCHAIN}" && touch "${BASE}/.built/_ndk") || exit 1
   fi
}

build() {
   what=$1

   if [[ ! -f "${BASE}/.built/${what}" ]]; then
       (/usr/bin/env bash --noprofile "${BASE}/_build_single.sh" "src/${what}.sh" && touch "${BASE}/.built/${what}") || exit 1
   fi
}


# Main.
[[ ! -d "${BASE}/.built" ]] && (mkdir "${BASE}/.built" || exit 1)

prepare_ndk
build bzip2-1.0.6
build xz-5.0.5
build openssl-1.0.0l
build Python-3.3.3

popd >/dev/null
