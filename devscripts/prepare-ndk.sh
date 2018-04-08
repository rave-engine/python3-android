#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 NDK_VER"
    exit 1
fi

# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

NDK_VER=$1
HOST_OS="$(uname | tr 'A-Z' 'a-z')"
NDK_ARCHIVE=android-ndk-$NDK_VER-$HOST_OS-x86_64.zip
wget --no-verbose https://dl.google.com/android/repository/$NDK_ARCHIVE
unzip -q $NDK_ARCHIVE

"$SCRIPTPATH"/strip-ndk.sh $(pwd)/android-ndk-$NDK_VER

rm -vf $NDK_ARCHIVE
