pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

autoreconf -i
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-shared || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
