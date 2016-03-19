#!/usr/bin/env bash
source ./env

# Stolen from https://github.com/rust-lang/rust/blob/2e2f53fad/configure#L345.
case $(uname -m) in
  i386 | i486 | i686 | i786 | x86)
      NDK_ARCH="x86"
      ;;
  x86-64 | x86_64 | x64 | amd64)
      NDK_ARCH="x86_64"
      ;;
  *)
      echo "Unknown architecture: $(uname -m)."
      exit 1
      ;;
esac

case "${NDK_REV}" in
  10*)
      NDK_EXT=bin
      ;;
  11*)
      NDK_EXT=zip
      ;;
  *)
      NDK_EXT=tar.bz2
      ;;
esac

if [ $SOURCES_LOCAL = 1 ]
then
  echo http://artifactory.ops.cld/artifactory/ThirdParty/COTS/android/android-ndk/r${NDK_REV}/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-${NDK_ARCH}.${NDK_EXT}
else
  case "${NDK_REV}" in
    11*)
        echo http://dl.google.com/android/repository/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-${NDK_ARCH}.${NDK_EXT}
        ;;
    *)
        echo http://dl.google.com/android/ndk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-${NDK_ARCH}.${NDK_EXT}
        ;;
  esac 
fi