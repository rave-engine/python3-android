Python 3 Android
================

This is an experimental set of build scripts that will cross-compile Python 3.9.0 for an Android device.

Prerequisites
-------------

Building requires:

1. Linux. This project might work on other systems supported by NDK but no guarantee.
2. Android NDK r21 installed and environment variable ``$ANDROID_NDK`` points to its root directory. Older NDK may not work and NDK <= r18 is known to be incompatible.
3. `python3.9` binary from Python 3.9.0 on the building host. It's recommended to use exactly that Python version, which can be installed via [pyenv](https://github.com/yyuu/pyenv). Don't forget to check that `python3.9` is available in $PATH.
4. `tic` binary from ncurses 6.2 on the building host. Slightly newer or older version may also work but no guarantee.
5. A case-sensitive filesystem. The default filesystem on Windows and macOS is case-insensitive, and building may fail.

Running requires:

1. Android 5.0 (Lollipop, API 21) or above
2. arm, arm64, x86 or x86-64

Build
-----

1. Run `./clean.sh` for good measure.
2. For every API Level/architecture combination you wish to build for:
   * `ARCH=arm ANDROID_API=21 ./build.sh` to build everything!

Build using Docker/Podman
------------------

Download the latest NDK for Linux from https://developer.android.com/ndk/downloads and extract it.

```
docker run --rm -it -v $(pwd):/python3-android -v /path/to/android-ndk:/android-ndk:ro --env ARCH=arm --env ANDROID_API=21 python:3.9.0-slim /python3-android/docker-build.sh
```

Here `/path/to/android-ndk` should be replaced with the actual for NDK (e.g., `/opt/android-ndk`).

Podman is also supported. Simply replace `docker` with `podman` in the command above.

Installation
------------

1. Make sure `adb shell` works fine
2. Copy all files in `build` to a folder on the device (e.g., ```/data/local/tmp/python3```). Note that on most devices `/sdcard` is not on a POSIX-compliant filesystem, so the python binary will not run from there.
3. In adb shell:
<pre>
cd /data/local/tmp/build
. ./env.sh
python3
</pre>
   And have fun!

SSL/TLS
-------
SSL certificates have old and new naming schemes. Android uses the old scheme yet the latest OpenSSL uses the new one. If you got ```CERTIFICATE_VERIFY_FAILED``` when using SSL/TLS in Python, you need to collect system certificates: (thanks @GRRedWings for the idea)
```
cd /data/local/tmp/build
mkdir -p etc/ssl
cat /system/etc/security/cacerts/* > etc/ssl/cert.pem
```
Path for certificates may vary with device vendor and/or Android version. Note that this approach only collects system certificates. If you need to collect user-installed certificates, most likely root access on your Android device is needed.

Check SSL/TLS functionality with:
```
import urllib.request
print(urllib.request.urlopen('https://httpbin.org/ip').read().decode('ascii'))
```


Known Issues
------------

No big issues! yay
