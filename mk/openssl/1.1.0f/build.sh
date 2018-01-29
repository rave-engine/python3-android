pushd src >/dev/null

rm -rf "${PACKAGE}"
tar -xf "${PACKAGE}.tar.gz" || exit 1
pushd "${PACKAGE}" >/dev/null

[[ ! -d "${PREFIX}/share" ]] && (mkdir "${PREFIX}/share" || exit 1)
patch -p1 < "${FILESDIR}/${PACKAGE}-ndk-clang-targets.patch" || exit 1
#patch -p1 < "${FILESDIR}/${PACKAGE}-sh.patch" || exit 1
#./Configure --prefix="${PREFIX}" --openssldir="${PREFIX}/share" android64-aarch64-clang 'no-shared' || exit 1
./Configure --prefix="${PREFIX}" --openssldir="${PREFIX}/share" "${ANDROID_TARGET}-clang" 'no-shared' || exit 1

make || exit 1
make install_sw || exit 1

# Remove binaries from premises.
rm -f "${PREFIX}/bin/"{openssl,c_rehash} || exit 1

popd >/dev/null
popd >/dev/null
