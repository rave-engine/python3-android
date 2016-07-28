patch -p1 < "${FILESDIR}/makefile-env.patch"
CFLAGS="$CPPFLAGS $CFLAGS" make clean
CFLAGS="$CPPFLAGS $CFLAGS" make libbz2.a bzip2 bzip2recover
CFLAGS="$CPPFLAGS $CFLAGS" make install
