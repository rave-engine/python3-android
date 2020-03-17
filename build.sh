#!/bin/sh
THIS_DIR="$PWD"

COMMON_ARGS="--arch ${ARCH:-arm} --api ${ANDROID_API:-21}"

[ -d src/cpython ] || git clone https://github.com/python/cpython src/cpython

cp -r Android src/cpython/
pushd src/cpython
./Android/build_deps.py $COMMON_ARGS
./Android/configure.py $COMMON_ARGS --prefix=/usr
make
make install DESTDIR="$THIS_DIR/build"
popd
cp -r src/cpython/Android/sysroot/usr/share/terminfo build/usr/share/
cp devscripts/env.sh build/
