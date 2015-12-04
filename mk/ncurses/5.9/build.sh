pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

patch -p1 < "${FILESDIR}/${PACKAGE}-android-locale-fixes.patch"
patch -p1 < "${FILESDIR}/${PACKAGE}-fix-bash-syntax-error.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --without-ada --without-manpages --without-progs --without-tests --without-termlib --enable-termcap --enable-widec --disable-database --disable-home-terminfo --with-shared --without-normal --without-debug --without-shlib-version --without-cxx-binding || exit 1
make || exit 1
make install || exit 1
# Fix symlinks for Python _curses and _curses_panel extensions.
ln -s ncursesw/curses.h "${PREFIX}/include/curses.h" || exit 1
ln -s ncursesw/panel.h "${PREFIX}/include/panel.h" || exit 1

popd >/dev/null
popd >/dev/null
