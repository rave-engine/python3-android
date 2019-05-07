Python 3 Android
================

This is an experimental set of build scripts that will cross-compile the latest Python 3 git master for an Android device.

Build status:

| System            | Status        |
| ----------------- |---------------|
| Linux (buildbot)  | [![Build Status](https://ci.chyen.cc/badges/python3-android.svg)](https://ci.chyen.cc/#/builders/python3-android) |

Prerequisites
-------------

Building requires:

1. Linux. This project might work on other Unix-like systems but no guarantee.
2. Android NDK r19 beta 1 or newer installed and environment variable ``$ANDROID_NDK`` points to its root directory. NDk r18 or below is not supported.
3. git and python3.8 in $PATH. It's recommended to use the latest git-master to build python3.8. Here are some ways to install the python3.8:
* For Arch Linux users, install [python-git](https://aur.archlinux.org/packages/python-git) package from AUR
* For other users, install 3.8 from [pyenv](https://github.com/yyuu/pyenv)
4. (Optional yet highly recommended) Vinay Sajip's [python-gnupg](https://bitbucket.org/vinay.sajip/python-gnupg) package for verifying PGP signatures of source tarballs and patches. You can install it with the following command:
```
python -m pip install --user python-gnupg
```
If pip is not installed, the ensurepip module is your friend:
```
python -m ensurepip --user
```

Running requires:

1. Android 5.0 (Lollipop, API 21) or above
2. arm, arm64, x86 or x86-64
3. A `busybox` binary at /data/local/tmp/busybox

Build
-----

1. `make clean` for good measure.
2. For every API Level/architecture combination you wish to build for:
   * Edit `pybuild/env.py` to match your (desired) configuration.
   * `make` to build everything!


Installation
------------

1. Make sure `adb shell` works fine
2. ```bash ./devscript/send.sh``` copies all files to ```/data/local/tmp/python3``` on the device
3. In adb shell:
<pre>
cd /data/local/tmp
. ./python3/tools/env.sh
python3.8m
</pre>
   And have fun!

SSL/TLS
-------
SSL certificates have old and new naming schemes. Android uses the old scheme yet the latest OpenSSL uses the new one. If you got ```CERTIFICATE_VERIFY_FAILED``` when using SSL/TLS in Python, you need to generating certificate names of the new scheme:
```
python3.8m ./python3/tools/c_rehash.py
```
Check SSL/TLS functionality with:
```
python3.8m ./python3/tools/ssl_test.py
```


Known Issues
------------

No big issues! yay
