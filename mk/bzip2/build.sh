export CFLAGS="$CPPFLAGS $CFLAGS" 

make libbz2.a bzip2 bzip2recover
make install PREFIX="$DESTDIR/usr"
