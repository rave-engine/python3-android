pushd src >/dev/null

rm -rf xz-5.0.5
tar -xf xz-5.0.5.tar.xz || exit 1
pushd xz-5.0.5 >/dev/null

./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-xz --disable-xzdec --disable-lzmadec --disable-lzmainfo --disable-lzma-links --disable-scripts || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
