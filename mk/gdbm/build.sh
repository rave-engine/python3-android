patch -p1 < "${FILESDIR}/disable-so-versioning.patch"
autoreconf --install --verbose --symlink --force
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --enable-libgdbm-compat || exit 1
make || exit 1
make install || exit 1
