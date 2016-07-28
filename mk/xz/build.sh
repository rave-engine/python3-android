patch -p1 < "${FILESDIR}/disable-so-versioning.patch" || exit 1
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-shared --disable-xz --disable-xzdec --disable-lzmadec --disable-lzmainfo --disable-lzma-links --disable-scripts || exit 1
make || exit 1
make install || exit 1
# Remove documentation.
rm -rf "${PREFIX}/share/doc"
