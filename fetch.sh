#!/usr/bin/env bash
source ./env

[[ ! -f "$BASE/sdk/android-ndk-r${NDK_REV}.tar.bz2" ]] && (wget http://dl.google.com/android/ndk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-$(uname -m).tar.bz2 -O "$BASE/sdk/android-ndk-r${NDK_REV}.tar.bz2" || exit 1)
[[ ! -f "$BASE/src/bzip2-1.0.6.tar.gz" ]] && (wget http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz -O "$BASE/src/bzip2-1.0.6.tar.gz" || exit 1)
[[ ! -f "$BASE/src/openssl-1.0.0l.tar.gz" ]] && (wget https://www.openssl.org/source/openssl-1.0.0l.tar.gz -O "$BASE/src/openssl-1.0.0l.tar.gz" || exit 1)
[[ ! -f "$BASE/src/Python-3.3.3.tar.xz" ]] && (wget http://python.org/ftp/python/3.3.3/Python-3.3.3.tar.xz -O "$BASE/src/Python-3.3.3.tar.xz" || exit 1)
[[ ! -f "$BASE/src/xz-5.0.5.tar.xz" ]] && (wget http://tukaani.org/xz/xz-5.0.5.tar.xz -O "$BASE/src/xz-5.0.5.tar.xz" || exit 1)
