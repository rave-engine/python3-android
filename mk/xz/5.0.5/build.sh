pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.xz" || exit 1
pushd "${PACKAGE}" >/dev/null

./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-xz --disable-xzdec --disable-lzmadec --disable-lzmainfo --disable-lzma-links --disable-scripts || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
