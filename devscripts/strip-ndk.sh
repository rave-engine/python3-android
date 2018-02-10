#!/bin/sh

# ** WARNING **
# This script aims to generate a minimum NDK for building python3-android
# It's not intended for general use!

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/ndk"
    exit 1
fi

NDK=$1

rm -rvf $NDK/sources

rm -rvf $NDK/platforms/android-*/arch-*/usr/include
rm -rvf $NDK/platforms/android-*/arch-*/usr/lib*/*.a

rm -rvf $NDK/toolchains/mips*
rm -rvf $NDK/sysroot/usr/include/mips*
rm -rvf $NDK/platforms/android-*/arch-mips*

rm -rvf $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/libexec
rm -rvf $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/bin/*{gcc,g++,c++,c++filt}*

# Files in bin/ are the same as triplet-prefixed binaries in ../../bin,
# while they shouldn't be deleted as they're used by clang
for bin in $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/*/bin ; do
    triplet=$(basename $(dirname $bin))
    for prog in ar as ld ld.bfd ld.gold nm objcopy objdump ranlib readelf strip ; do
        ln -sf ../../bin/$triplet-$prog $bin/$prog
    done
done

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

rm -rvf $NDK/toolchains/llvm/prebuilt/linux-x86_64/test
rm -rvf $NDK/toolchains/llvm/prebuilt/linux-x86_64/lib64/clang/$clang_version/lib/linux/*{asan,tsan,ubsan}*
rm -rvf $NDK/toolchains/llvm/prebuilt/linux-x86_64/lib64/clang/$clang_version/lib/linux/*/{libFuzzer,libomp}.a
rm -vf $NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/{clang-format,clang-tidy,sancov}
# libffi requires CXXCPP
rm -vf $NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/clang++
ln -s clang $NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/clang++

rm -rvf $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/lib/lib64/{libc++,libLLVM}.so
rm -rvf $NDK/toolchains/*-4.9/prebuilt/linux-x86_64/lib/bfd-plugins/LLVMgold.so
