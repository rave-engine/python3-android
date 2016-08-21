./configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --without-ada \
    --without-manpages \
    --without-progs \
    --without-tests \
    --without-termlib \
    --enable-termcap \
    --enable-widec \
    --with-shared \
    --without-normal \
    --without-debug \
    --without-cxx-binding \
    --enable-overwrite \
    --without-curses-h \
    --with-warnings

make
make install
