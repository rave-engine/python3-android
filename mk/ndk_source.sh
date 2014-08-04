#!/usr/bin/env bash

source ./env
echo http://dl.google.com/android/ndk/android-ndk-r${NDK_REV}-$(uname -s | tr '[A-Z]' '[a-z'])-$(uname -m).tar.bz2
