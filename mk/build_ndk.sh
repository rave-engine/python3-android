#!/usr/bin/env bash
source ./env

# Stolen from https://github.com/rust-lang/rust/blob/2e2f53fad/configure#L345.
case $(uname -m) in
  i386 | i486 | i686 | i786 | x86)
      NDK_ARCH="x86"
      ;;
  x86-64 | x86_64 | x64 | amd64)
      NDK_ARCH="x86_64"
      ;;
  *)
      echo "Unknown architecture: $(uname -m)."
      exit 1
      ;;
esac

[[ ! -d "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_PREFIX}/.built-${BUILD_IDENTIFIER}" || exit 1)
[[ ! -d "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" ]] && (mkdir -p "${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" || exit 1)

[[ ! -d "$BASE/sdk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z]')-${NDK_ARCH}.bin" ]] && (chmod a+x "$BASE/sdk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z]')-${NDK_ARCH}.bin" || exit 1)
[[ ! -d "$BASE/sdk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z]')-${NDK_ARCH}.bin" ]] && ("$BASE/sdk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z]')-${NDK_ARCH}.bin" || exit 1)

[[ ! -d "$BASE/android-ndk-r${NDK_REV}" ]] && ("mv -f $BASE/android-ndk-r${NDK_REV} $BASE/sdk/android-ndk-r${NDK_REV}" || exit 1)

if [[ ! -f "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}" ]]; then
    ("${BASE}/sdk/${NDK_REL}/build/tools/make-standalone-toolchain.sh" --platform="android-${ANDROID_API_LEVEL}" --install-dir="${ANDROID_TOOL_PREFIX}/${BUILD_IDENTIFIER}" --toolchain="${ANDROID_TOOLCHAIN}" &&\
     touch "${ANDROID_PREFIX}/.built-ndk-${BUILD_IDENTIFIER}") || exit 1
fi
