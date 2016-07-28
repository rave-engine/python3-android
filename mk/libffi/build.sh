patch -p1 < "${FILESDIR}/libffi-pr240-modded.patch" || exit 1

./autogen.sh

./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" || exit 1
make || exit 1
make install || exit 1
