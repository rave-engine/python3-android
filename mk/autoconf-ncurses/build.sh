./configure \
    --prefix="${ANDROID_PREFIX}/host/usr"

make
make install DESTDIR=
