autoreconf --install --verbose --force

cd build-target

CONFIG_SITE="${FILESDIR}/config.site" \
../configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-ipv6 \
    --with-system-ffi
make
make altinstall
