pushd src >/dev/null

rm -rf bzip2-1.0.6
tar -xf bzip2-1.0.6.tar.gz || exit 1
pushd bzip2-1.0.6 >/dev/null

patch -p1 < "$BASE/mk/bzip2/1.0.6/bzip2-1.0.6-makefile-env.patch" || exit 1
make clean || exit 1
make libbz2.a || exit 1
make install_libbz2.a || exit 1

popd >/dev/null
popd >/dev/null
