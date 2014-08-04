#!/usr/bin/env bash
source ./env

# Install the SDK manager.
if [[ ! -d "$BASE/sdk/android-sdk-r${SDK_REV}" ]]; then
    case $(uname -s) in
    Darwin)
        [[ ! -f "$BASE/sdk/android-sdk-r${SDK_REV}.zip" ]] && (wget http://dl.google.com/android/android-sdk_r${SDK_REV}-macosx.zip -O "$BASE/sdk/android-sdk-r${SDK_REV}.zip" || exit 1)
        unzip -q "$BASE/sdk/android-sdk-r${SDK_REV}.zip" -d "$BASE/sdk" || exit 1
        mv "$BASE/sdk/android-sdk-macosx" "$BASE/sdk/android-sdk-r${SDK_REV}" || exit 1
        ;;
    Linux)
        [[ ! -f "$BASE/sdk/android-sdk-r4{SDK_REV}.zip" ]] && (wget http://dl.google.com/android/android-sdk_r${SDK_REV}-linux.tgz -O "$BASE/sdk/android-sdk-r${SDK_REV}.tgz" || exit 1)
        tar -xf "$BASE/sdk/android-sdk-r${SDK_REV}.tgz" -C "$BASE/sdk" || exit 1
        mv "$BASE/sdk/android-sdk-linux" "$BASE/sdk/android-sdk-r${SDK_REV}" || exit 1
        ;;
    esac
fi

pushd "$BASE/sdk/android-sdk-r${SDK_REV}" > /dev/null

# Find SDK platform ID to use.
SDK_ID=$(./tools/android -s list sdk -a        |\
         grep -F 'SDK Platform Android'        |\
         grep -Fm1 "API ${ANDROID_API_LEVEL}"  |\
         awk '{print $1}' | tr -d '-')
if [[ -z "${SDK_ID}" ]]; then
    echo "Could not find SDK package for API level ${ANDROID_API_LEVEL}, make sure it's available using:"
    echo "  $BASE/sdk/android-sdk-r${SDK_REV}/tools/android list sdk"
    echo "and check if it's in there."
    exit 1
fi
# Install base SDKs.
echo "${ANDROID_AGREE_LICENSE_TERMS}" | ./tools/android -s update sdk --no-ui -a --filter "${SDK_ID},tool,platform-tool" || exit 1

# Get SDK system image ID.
case "${ANDROID_PLATFORM}" in
  arm)
      ABI_SEARCH_TERM="ARM EABI"
      ABI_OPT="armeabi-v7a"
      ;;
  x86)
      ABI_SEARCH_TERM="Intel x86"
      ABI_OPT="x86"
      ;;
  *)
      echo "Unknown Android platform: ${ANDROID_PLATFORM}"
      exit 1
      ;;
esac
ABI_IMG_ID=$(./tools/android -s list sdk -a            |\
             grep -F 'System Image'                    |\
             grep -F "${ABI_SEARCH_TERM}"              |\
             grep -Fm1 "API ${ANDROID_API_LEVEL}"      |\
             awk '{print $1}' | tr -d '-')
if [[ -z "${ABI_IMG_ID}" ]]; then
    echo "Could not find ${ABI_SEARCH_TERM} system image for API level ${ANDROID_API_LEVEL}, make sure it's available using:"
    echo "  $BASE/sdk/android-sdk-r${SDK_REV}/tools/android list sdk"
    echo "and check if it's in there."
    exit 1
fi

# Install SDK system image
echo "${ANDROID_AGREE_LICENSE_TERMS}" | ./tools/android -s update sdk --no-ui -a --filter "${ABI_IMG_ID}" || exit 1

# Make a VM.
[[ ! -d "${ANDROID_TEST_PREFIX}" ]] && (mkdir "${ANDROID_TEST_PREFIX}" || exit 1)
echo n | ./tools/android -s create avd -f                                 \
    -t "android-${ANDROID_API_LEVEL}"                                     \
    -n "${ANDROID_VM_NAME}-${TEST_IDENTIFIER}"                            \
    -p "${ANDROID_TEST_PREFIX}/${TEST_IDENTIFIER}"                        \
    -b "${ABI_OPT}"                                                       \
|| exit 1

# We're done here.
popd > /dev/null
