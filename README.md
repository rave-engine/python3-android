Python 3 Android
================

This is an experimental set of build scripts that will crosscompile Python 3 for an ARM Android device.

Usage
------

1. Download the [Android NDK](https://developer.android.com/tools/sdk/ndk/index.html) and extract `android-ndk-r$V` to the `sdk` directory.
2. Edit `env` to match your configuration.
3. Run `./clean.sh` for good measure.
4. Run `./fetch.sh` to fetch the source archives.
5. Run `./build.sh` to build everything!

Currently, cross-compiling is only supported for Linux hosts due Python cross-compile limitations. 
