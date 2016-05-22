pushd src >/dev/null

rm -rf "${NAME}-autoconf-3130000"
tar -xf "${NAME}-autoconf-3130000.tar.gz" || exit 1
pushd "${NAME}-autoconf-3130000" >/dev/null

./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-shared || exit 1
make || exit 1
make install || exit 1

# Remove binary from premises.
rm -f "${PREFIX}/bin/sqlite3" || exit 1

popd >/dev/null
popd >/dev/null
