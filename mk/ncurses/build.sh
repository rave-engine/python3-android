./configure \
    --host="${TARGET}" \
    --build="${HOST}" \
    --without-ada \
    --without-manpages \
    --without-progs \
    --without-tests \
    --without-termlib \
    --enable-termcap \
    --enable-widec \
    --without-shared \
    --with-normal \
    --without-debug \
    --without-cxx-binding \
    --without-curses-h \
    --with-warnings

make
make install
