./configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-static
make
make install
