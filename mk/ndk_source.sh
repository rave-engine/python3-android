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

# NOTE: For newer is seems that we require to unzip
case "${NDK_REV}" in
  10*)
      NDK_EXT=bin
      ;;
  13*)
      NDK_EXT=zip
      ;;
  *)
      NDK_EXT=tar.bz2
      ;;
esac


case "${NDK_EXT}" in
  zip)
	echo http://dl.google.com/android/repository//android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-${NDK_ARCH}.${NDK_EXT}
	;;
  *)
	echo http://dl.google.com/android/ndk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-${NDK_ARCH}.${NDK_EXT}
	;;
esac
