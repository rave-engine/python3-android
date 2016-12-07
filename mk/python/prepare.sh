patch -F0 -p1 -i "${FILESDIR}/check-crypt.patch"
patch -F0 -p1 -i "${FILESDIR}/gdbm.patch"
patch -F0 -p1 -i "${FILESDIR}/decimal.patch"
patch -F0 -p1 -i "${BASE}/src/ncurses-headers.patch"
patch -F0 -p1 -i "${BASE}/src/android-locale-utf8.patch"
patch -F0 -p1 -i "${BASE}/src/0001-setup.py-do-not-add-invalid-header-locations.patch"

mkdir build-target
