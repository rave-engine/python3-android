CHOST="${ANDROID_TARGET}-" \
./configure \
    --prefix=/usr \
    --static
make
make install
