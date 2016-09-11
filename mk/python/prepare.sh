patch -F0 -p1 -i "${FILESDIR}/check-crypt.patch"

rm -rf Modules/_ctypes/{darwin,libffi}*

mkdir build-target
