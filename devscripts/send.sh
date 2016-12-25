set -e
set -x

TMP=/data/local/tmp

./devscripts/package.sh

cd build

adb shell rm /sdcard/python3-android.tar
adb push python3-android.tar /sdcard/python3-android.tar

adb shell rm -rf $TMP/python3
adb shell tar xvf /sdcard/python3-android.tar -C $TMP
adb shell mv $TMP/target $TMP/python3
