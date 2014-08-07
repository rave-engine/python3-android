pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

patch -p1 < "${FILESDIR}/${PACKAGE}-makefile-env.patch" || exit 1
make clean || exit 1
make libbz2.a || exit 1
make install_libbz2.a || exit 1

popd >/dev/null
popd >/dev/null
