pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

for i in {001..008} ; do
    patch -p0 < "${BASE}/src/readline63-$i" || exit 1
done
patch -p1 < "${FILESDIR}/build-unversioned-so.patch" || exit 1

autoreconf -i
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-static || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
