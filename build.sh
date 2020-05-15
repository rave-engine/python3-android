#!/bin/bash

set -e
set -x

THIS_DIR="$PWD"

PYVER=3.9.0a6
PYVER_SHORT=3.9.0
SRCDIR=src/Python-$PYVER

COMMON_ARGS="--arch ${ARCH:-arm} --api ${ANDROID_API:-21}"

if [ ! -d $SRCDIR ]; then
    mkdir -p src
    pushd src
    curl -vLO https://www.python.org/ftp/python/$PYVER_SHORT/Python-$PYVER.tar.xz
    tar xf Python-$PYVER.tar.xz
    popd
fi

cp -r Android $SRCDIR
pushd $SRCDIR
./Android/build_deps.py $COMMON_ARGS
./Android/configure.py $COMMON_ARGS --prefix=/usr
make
make install DESTDIR="$THIS_DIR/build"
popd
cp -r $SRCDIR/Android/sysroot/usr/share/terminfo build/usr/share/
cp devscripts/env.sh build/
