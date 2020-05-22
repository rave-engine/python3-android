FROM python:3.9.0b1-buster

ARG NDK_VER=r21b

RUN apt-get update -y && \
    apt-get install -y autoconf automake cmake gawk gettext git gcc make patch pkg-config

ADD https://dl.google.com/android/repository/android-ndk-${NDK_VER}-linux-x86_64.zip /

RUN unzip android-ndk-${NDK_VER}-linux-x86_64.zip

WORKDIR /python3-android
ENV ANDROID_NDK=/android-ndk-${NDK_VER}

CMD ["/python3-android/build.sh"]
