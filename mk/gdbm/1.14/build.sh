pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

patch -p1 < "${FILESDIR}/${PACKAGE}-android-winsize.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --enable-libgdbm-compat || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
