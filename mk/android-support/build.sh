pushd src

rm -rf "${NAME}"
cp -rv "$ANDROID_NDK/sources/android/support" "${NAME}"
pushd "${NAME}"

set -e
ndk-build NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=Android.mk TARGET_PLATFORM=android-${ANDROID_API_LEVEL} V=1
mkdir "${PREFIX}"/{lib,include/${NAME}}
cp ./obj/local/armeabi/libandroid_support.a "${PREFIX}/lib/"
cp -r include/* "${PREFIX}/include/${NAME}"

popd
popd
