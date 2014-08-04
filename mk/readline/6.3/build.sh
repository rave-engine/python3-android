pushd src >/dev/null

rm -rf readline-6.3
tar -xf readline-6.3.tar.gz || exit 1
pushd readline-6.3 >/dev/null

autoreconf -i
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
