pushd src/libffi || exit 1

git checkout .
git clean -dfx

./autogen.sh

./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" || exit 1
make || exit 1
make install || exit 1

popd >/dev/null

