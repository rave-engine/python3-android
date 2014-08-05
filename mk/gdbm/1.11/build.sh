pushd src >/dev/null

rm -rf gdbm-1.11
tar -xf gdbm-1.11.tar.gz || exit 1
pushd gdbm-1.11 >/dev/null

patch -p1 < "${BASE}/mk/gdbm/1.11/gdbm-1.11-android-winsize.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --enable-libgdbm-compat || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
