set -e
set -x

source ./env

NAME=${BUILD_IDENTIFIER}
TMP=/data/local/tmp

./devscripts/package.sh

cd build

adb shell rm /sdcard/${NAME}.tar
adb push ${NAME}.tar /sdcard/${NAME}.tar

adb shell rm -rf $TMP/python3
adb shell tar xvf /sdcard/${NAME}.tar -C $TMP
adb shell mv $TMP/${NAME} $TMP/python3
