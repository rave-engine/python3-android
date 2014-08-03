Python 3 Android
================

This is an experimental set of build scripts that will crosscompile Python 3 for an ARM Android device.

Usage
------

1. Run `./clean.sh` for good measure.
2. For every NDK/API Level/Toolchain combination you wish to build for:
   * Edit `env` to match your (desired) configuration.
   * Run `./fetch.sh` to fetch the NDK and needed source archives.
   * Run `./build.sh` to build everything!
   * (Optional) run `./test.sh` to setup an Android emulator and run automated Python regression tests.
   * Run `./clean-generated.sh` to clean things up for the next build.

Currently, cross-compiling is only supported for Linux hosts due Python cross-compile limitations. 

Requirements
------------

Building requires:

1. A working host toolchain that is able to compile Python (for hostpython).
2. Patience.

Testing requires:

1. Java 6 to use the Android SDK manager.
2. `awk` and `tr` for some setup wizardry.
3. Even more patience.

Both require:

1. A working `bash` and basic *nix utilities like `cp` and `touch`.
2. `wget` to fetch files.
2. `tar` to extract files.
