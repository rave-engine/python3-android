CHOST="${ANDROID_TARGET}-" \
CFLAGS="${CPPFLAGS} ${CFLAGS}"
./configure \
    --prefix=/usr \
    --static
make
make install
