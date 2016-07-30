mkdir -p "${PREFIX}/share"
patch -p1 < "${FILESDIR}/android-ndk-target.patch"
patch -p1 < "${FILESDIR}/disable-libversion.patch"
