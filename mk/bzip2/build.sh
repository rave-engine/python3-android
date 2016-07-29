export CFLAGS="$CPPFLAGS $CFLAGS" 

patch -p1 < "${FILESDIR}/makefiles.patch"

make clean
make bzip2recover
make -f Makefile-libbz2_so

make install
cp -f bzip2-shared "${PREFIX}/bin/bzip2"
cp -f libbz2.so "${PREFIX}/lib/libbz2.so"
