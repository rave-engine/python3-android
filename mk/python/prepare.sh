patch -p1 < "${FILESDIR}/python-misc.patch"
patch -p1 < "${FILESDIR}/android-misc.patch"
patch -p1 < "${FILESDIR}/check-crypt.patch"

rm -rf Modules/_ctypes/{darwin,libffi}*

mkdir build-target
