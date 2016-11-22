patch -F0 -p1 -i "${FILESDIR}/check-crypt.patch"
patch -F0 -p1 -i "${FILESDIR}/ncurses-headers.patch"
patch -F0 -p1 -i "${FILESDIR}/android-locale-utf8.patch"

mkdir build-target
