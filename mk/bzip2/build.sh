patch -p1 < "${FILESDIR}/makefile-env.patch" || exit 1
CFLAGS="$CPPFLAGS $CFLAGS" make clean || exit 1
CFLAGS="$CPPFLAGS $CFLAGS" make libbz2.a bzip2 bzip2recover || exit 1
CFLAGS="$CPPFLAGS $CFLAGS" make install || exit 1
