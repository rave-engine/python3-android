case "$ANDROID_PLATFORM" in
    arm)    openssl_target=android-armeabi;;
    arm64)  openssl_target=android64-aarch64;;
    x86)    openssl_target=android-x86;;
    x86_64) openssl_target=android64-x86_64;;
    mips)   openssl_target=android-mips;;
    mips64) openssl_target=android64-mips64;;
esac
export OPENSSL_CFLAGS="$CFLAGS"
./Configure "$openssl_target" no-shared --prefix=/usr --openssldir=/etc/ssl
make
make install_sw install_ssldirs
