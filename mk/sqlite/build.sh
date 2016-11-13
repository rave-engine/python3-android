./configure \
    --prefix=/usr \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-shared
make
make install
