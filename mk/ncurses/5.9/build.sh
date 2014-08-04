pushd src >/dev/null

rm -rf ncurses-5.9
tar -xf ncurses-5.9.tar.gz || exit 1
pushd ncurses-5.9 >/dev/null

patch -p1 < "$BASE/mk/ncurses/5.9/ncurses-5.9-android-locale-fixes.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --without-ada --without-manpages --without-progs --without-tests --with-termlib --enable-widec || exit 1
make || exit 1
make install || exit 1
# Fix symlinks for Python _curses and _curses_panel extensions.
ln -s ncursesw/curses.h "${PREFIX}/curses.h"
ln -s ncursesw/panel.h "${PREFIX}/panel.h"

popd >/dev/null
popd >/dev/null
