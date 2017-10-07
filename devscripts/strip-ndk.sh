#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/ndk"
    exit 1
fi

NDK=$1

rm -rvf $NDK/sources

rm -rvf $NDK/platforms/android-*/arch-*/usr/include
rm -rvf $NDK/platforms/android-*/arch-*/usr/lib*/*.a

rm -rvf $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/libexec

rm -rvf $NDK/toolchains/renderscript

rm -rvf $NDK/prebuilt/android-*

rm -rvf $NDK/{simpleperf,shader-tools}

rm -rvf $NDK/prebuilt/linux-x86_64/bin/{py*,2to3,idle}
rm -rvf $NDK/prebuilt/linux-x86_64/include/python2.7/
rm -rvf $NDK/prebuilt/linux-x86_64/lib/*python2.7*
rm -rvf $NDK/python-packages

rm -rvf $NDK/platforms/android-{9,1*}

clang_version=$(cat $NDK/toolchains/llvm/prebuilt/linux-x86_64/AndroidVersion.txt)
clang_version_no_patch=$(echo $clang_version | sed 's/\.[0-9]\{1,\}$//')
rm -rvf $NDK/toolchains/llvm/prebuilt/linux-x86_64/lib64/clang/$clang_version_no_patch
ln -s $clang_version $NDK/toolchains/llvm/prebuilt/linux-x86_64/lib64/clang/$clang_version_no_patch

rm -vf $NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/clang++
ln -s clang $NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/clang++

rm -rvf $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/lib/lib64/{libc++,libLLVM}.so
