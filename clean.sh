source ./env

./clean-build.sh
rm -rf "$ANDROID_PREFIX"
rm -rf "$ANDROID_TEST_PREFIX"
rm -rf "$ANDROID_TOOL_PREFIX"

