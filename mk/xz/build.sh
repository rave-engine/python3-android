patch -p1 < "${FILESDIR}/disable-so-versioning.patch"
./configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-static
make
make install
