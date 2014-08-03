source ./env

./clean-generated.sh
./clean-builds.sh
rm -rf "$ANDROID_TEST_PREFIX"
rm -rf "$ANDROID_TOOL_PREFIX"

