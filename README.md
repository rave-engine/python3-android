Python 3 Android
================

This is an experimental set of build scripts that will cross-compile the latest Python 3 hg tip for an Android device.

Prerequisites
-------------

Building requires:

1. Linux or macOS. Ubuntu 14.04, Arch Linux and macOS Sierra tested.
2. Android NDK r14 beta 1 or above installed and environment variable ``$ANDROID_NDK`` points to its root directory. NDk r13 or below is not supported.
3. git, hg and python3.7 in $PATH

Running requires:

1. Android 5.0 (Lollipop, API 21) or above
2. arm, arm64, x86, x86-64, MIPS or MIPS64

Build
-----

1. `make clean` for good measure.
2. For every API Level/architecture combination you wish to build for:
   * Edit `env` to match your (desired) configuration.
   * `make` to build everything!


Installation
------------

1. Make sure `adb shell` works fine
2. ```bash ./devscript/send.sh``` copies all files to ```/data/local/tmp/python3``` on the device
3. In adb shell:
<pre>
cd /data/local/tmp
. ./python3/tools/env.sh
python3.7m
</pre>
   And have fun!

SSL/TLS
-------
SSL certificates have old and new naming schemes. Android uses the old scheme yet the latest OpenSSL uses the new one. If you got ```CERTIFICATE_VERIFY_FAILED``` when using SSL/TLS in Python, you need to generating certificate names of the new scheme:
```
python3.7m ./python3/tools/c_rehash.py
```
Check SSL/TLS functionality with:
```
python3.7m ./python3/tools/ssl_test.py
```


Known Issues
------------

No big issues! yay
