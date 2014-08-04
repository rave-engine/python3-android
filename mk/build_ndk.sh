#!/usr/bin/env bash
source ./env

[[ ! -d "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${BASE}/sdk/${NDK_REL}" ]] && (tar -xf "$BASE/sdk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z]')-$(uname -m).tar.bz2" -C "$BASE/sdk" || exit 1)

if [[ ! -f "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}" ]]; then
    ("${BASE}/sdk/${NDK_REL}/build/tools/make-standalone-toolchain.sh" --platform="android-${ANDROID_API_LEVEL}" --install-dir="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" --toolchain="${ANDROID_TOOLCHAIN}" &&\
     touch "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}") || exit 1
fi
