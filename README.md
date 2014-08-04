Python 3 Android
================

This is an experimental set of build scripts that will crosscompile Python 3 for an ARM Android device.

Usage
------

1. Run `./clean.sh` for good measure.
2. For every NDK/API Level/Toolchain combination you wish to build for:
   * Edit `env` to match your (desired) configuration.
   * `make` to build everything!
   * (Optional) `make test` to setup an Android emulator and run automated Python regression tests.

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

FAQ
---

*The build is failing with something about license terms!*

Read the license terms, edit `env` and set `ANDROID_AGREE_LICENSE_TERMS=y` if you agree with them, and re-run.
