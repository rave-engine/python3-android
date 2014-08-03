Python 3 Android
================

This is an experimental set of build scripts that will crosscompile Python 3 for an ARM Android device.

Usage
------

1. Edit `env` to match your (desired) configuration.
2. Run `./clean.sh` for good measure.
3. Run `./fetch.sh` to fetch the NDK and needed source archives.
4. Run `./build.sh` to build everything!
5. (Optional) run `./test.sh` to setup an Android emulator and run automated Python regression tests.

Currently, cross-compiling is only supported for Linux hosts due Python cross-compile limitations. 
