pushd src >/dev/null

rm -rf sqlite-autoconf-3080500
tar -xf sqlite-autoconf-3080500.tar.gz || exit 1
pushd sqlite-autoconf-3080500 >/dev/null

./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" || exit 1
make || exit 1
make install || exit 1

# Remove binary from premises.
rm -f "${PREFIX}/bin/sqlite3" || exit 1

popd >/dev/null
popd >/dev/null
