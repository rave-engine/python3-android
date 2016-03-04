set -x

source ./env

NAME=${BUILD_IDENTIFIER}
TMP=/data/local/tmp

cd build

mkdir -p $NAME/tools
cp ../devscripts/{c_rehash.py,env.sh} $NAME/tools

tar zcf ${NAME}.tar.gz $NAME
adb shell rm /sdcard/${NAME}.tar.gz
adb push ${NAME}.tar.gz /sdcard/${NAME}.tar.gz

adb shell rm -r $TMP/python3
adb shell tar zxvf /sdcard/${NAME}.tar.gz -C $TMP
adb shell mv $TMP/${NAME} $TMP/python3
