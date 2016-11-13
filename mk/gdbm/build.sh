./configure \
    --prefix=/usr \
    --host="${TARGET}" \
    --build="${HOST}" \
    --enable-libgdbm-compat \
    --disable-shared
make
make install
