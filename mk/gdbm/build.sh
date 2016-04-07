pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

patch -p1 < "${FILESDIR}/disable-so-versioning.patch"
patch -p1 < "${FILESDIR}/gdbmtool-h-missing-function.patch"
autoreconf --install --verbose --symlink --force
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --enable-libgdbm-compat || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
