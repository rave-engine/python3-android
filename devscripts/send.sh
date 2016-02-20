set -x

NAME=10e-16-arm-linux-androideabi-4.9
TMP=/data/local/tmp

cd build
tar zcf ${NAME}.tar.gz $NAME
adb shell rm /sdcard/${NAME}.tar.gz
adb push ${NAME}.tar.gz /sdcard/${NAME}.tar.gz

adb shell rm -r $TMP/python3
adb shell tar zxvf /sdcard/${NAME}.tar.gz -C $TMP
adb shell mv $TMP/${NAME} $TMP/python3
