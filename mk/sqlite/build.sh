./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-shared
make
make install

# Remove binary from premises.
rm -f "${PREFIX}/bin/sqlite3"
