source ./env

find "$BASE/src" -mindepth 1 -maxdepth 1 -type d -exec rm -rf "{}" \;
rm -rf "$ANDROID_PREFIX"
rm -rf "$ANDROID_TOOL_PREFIX"
rm -rf "$BASE/.built"
