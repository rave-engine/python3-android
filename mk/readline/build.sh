for i in {001..008} ; do
    patch -p0 < "${BASE}/src/readline63-$i"
done
patch -p1 < "${FILESDIR}/build-unversioned-so.patch"

autoreconf -i
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-static
make
make install
