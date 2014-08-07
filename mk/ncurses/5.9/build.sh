pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

patch -p1 < "${FILESDIR}/${PACKAGE}-android-locale-fixes.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --without-ada --without-manpages --without-progs --without-tests --with-termlib --enable-widec || exit 1
make || exit 1
make install || exit 1
# Fix symlinks for Python _curses and _curses_panel extensions.
ln -s ncursesw/curses.h "${PREFIX}/include/curses.h" || exit 1
ln -s ncursesw/panel.h "${PREFIX}/include/panel.h" || exit 1

popd >/dev/null
popd >/dev/null
