./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-shared || exit 1
make || exit 1
make install || exit 1

# Remove binary from premises.
rm -f "${PREFIX}/bin/sqlite3" || exit 1
