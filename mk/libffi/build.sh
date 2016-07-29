patch -p1 < "${FILESDIR}/libffi-pr240-modded.patch"

./autogen.sh

./configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-static
make
make install
