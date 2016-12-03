# Use Thomas Dickey's patched autoconf
patch -F0 -p1 -i "${FILESDIR}/skip-cc-env-check.patch"

PATH="$ANDROID_PREFIX/host/usr/bin:$PATH" autoreconf --install --verbose --force
