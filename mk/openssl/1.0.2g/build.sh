pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

[[ ! -d "${PREFIX}/share" ]] && (mkdir "${PREFIX}/share" || exit 1)
patch -p1 < "${FILESDIR}/${PACKAGE}-android-ndk-target.patch" || exit 1
patch -p1 < "${FILESDIR}/${PACKAGE}-disable-libversion.patch" || exit 1
./Configure android-ndk --prefix="${PREFIX}" --openssldir="${PREFIX}/share" || exit 1
make DISABLE_LIBVERSION=1 || exit 1
make DISABLE_LIBVERSION=1 install_sw || exit 1

# Remove binaries from premises.
rm -f "${PREFIX}/bin/"{openssl,c_rehash} || exit 1

popd >/dev/null
popd >/dev/null
