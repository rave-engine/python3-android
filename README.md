Python 3 Android
================

This is an experimental set of build scripts that will crosscompile the latest Python 3 hg tip for an Android device.

Usage
------

1. `make clean` for good measure.
2. For every API Level/architecture combination you wish to build for:
   * Edit `env` to match your (desired) configuration.
   * `make` to build everything!

Requirements
------------

Building requires:

1. Linux
2. The latest Android NDK installed and environment variable ``$ANDROID_NDK`` points to its root directory.
3. git, hg and python3.6 in $PATH

Known Issues
------------

1. Python is currently not usable. See https://bugs.python.org/issue28046
