pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

patch -p1 < "${FILESDIR}/fix-bash-syntax-error.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --without-ada --without-manpages --without-progs --without-tests --without-termlib --enable-termcap --enable-widec --disable-database --disable-home-terminfo --with-shared --without-normal --without-debug --without-shlib-version --without-cxx-binding --enable-overwrite || exit 1
make || exit 1
make install || exit 1

popd >/dev/null
popd >/dev/null
