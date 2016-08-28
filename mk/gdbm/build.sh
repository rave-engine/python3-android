./configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --enable-libgdbm-compat \
    --disable-shared
make
make install
