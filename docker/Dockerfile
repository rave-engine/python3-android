FROM archlinux/base

# Need to reinitialize pacman keyring; see https://github.com/archlinux/archlinux-docker/issues/18
RUN echo 'Server = https://mirror.pkgbuild.com/$repo/os/$arch' > /etc/pacman.d/mirrorlist && \
    echo $'[archlinuxcn]\nServer = https://repo.archlinuxcn.org/$arch' >> /etc/pacman.conf && \
    pacman-key --init && pacman-key --populate archlinux && \
    pacman -Syu --noconfirm && \
    pacman -S --noconfirm archlinuxcn-keyring && \
    pacman -S --noconfirm --needed android-ndk autoconf automake cmake gawk gettext git gcc make patch pkgconf python python-git which

WORKDIR /python3-android
# Set $ANDROID_NDK manually as /etc/profile.d/*.sh are not sourced by CMD
ENV ANDROID_NDK=/opt/android-ndk

CMD ["bash", "/python3-android/build.sh"]
