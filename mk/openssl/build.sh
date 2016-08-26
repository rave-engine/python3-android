case "$ANDROID_PLATFORM" in
    arm)    openssl_target=android-armeabi;;
    arm64)  openssl_target=android64-aarch64;;
    x86)    openssl_target=android-x86;;
    mips)   openssl_target=android-mips;;
esac
export OPENSSL_CFLAGS="$CFLAGS"
./Configure "$openssl_target" no-shared --prefix="${PREFIX}" --openssldir="${PREFIX}/share"
make
make install_sw
