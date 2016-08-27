patch -p1 < "${FILESDIR}/python-misc.patch"
patch -p1 < "${FILESDIR}/android-misc.patch"
patch -p1 < "${FILESDIR}/check-crypt.patch"
patch -p1 < "${BASE}/src/Port-Python-s-SSL-module-to-OpenSSL-1.1.0-3.patch"

rm -rf Modules/_ctypes/{darwin,libffi}*

mkdir build-target
