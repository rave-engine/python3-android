autoreconf --install --verbose --symlink --force
./configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --enable-libgdbm-compat \
    --disable-static
make
make install
