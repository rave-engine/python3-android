#!/usr/bin/env bash
source ./env

[[ ! -d "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)

if [[ ! -f "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}" ]]; then
    ("${ANDROID_NDK}/build/tools/make-standalone-toolchain.sh" --platform="android-${ANDROID_API_LEVEL}" --install-dir="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" --toolchain="${ANDROID_TOOLCHAIN}" &&\
     touch "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}") || exit 1
fi
