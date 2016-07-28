patch -p1 < "${FILESDIR}/disable-so-versioning.patch"
./configure --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-shared --disable-xz --disable-xzdec --disable-lzmadec --disable-lzmainfo --disable-lzma-links --disable-scripts
make
make install
# Remove documentation.
rm -rf "${PREFIX}/share/doc"
