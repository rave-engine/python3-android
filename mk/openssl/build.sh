[[ ! -d "${PREFIX}/share" ]] && (mkdir "${PREFIX}/share")
patch -p1 < "${FILESDIR}/android-ndk-target.patch"
patch -p1 < "${FILESDIR}/disable-libversion.patch"
./Configure android-ndk --prefix="${PREFIX}" --openssldir="${PREFIX}/share"
make DISABLE_LIBVERSION=1
make DISABLE_LIBVERSION=1 install_sw

# Remove binaries from premises.
rm -f "${PREFIX}/bin/"{openssl,c_rehash}
