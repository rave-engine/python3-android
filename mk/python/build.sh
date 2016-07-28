# Apply patches and build target Python.
cat > config.site <<-SITE
	ac_cv_file__dev_ptmx=no
	ac_cv_file__dev_ptc=no
SITE

patch -p1  < "${FILESDIR}/cross-compile.patch"
patch -p1  < "${FILESDIR}/python-misc.patch"
patch -p1  < "${FILESDIR}/android-misc.patch"
patch -p1  < "${FILESDIR}/android-l-pie.patch"

rm -rf Modules/_ctypes/{darwin,libffi}*

autoreconf --install --verbose --force

mkdir build-target && pushd build-target
PATH="$(pwd)/../build-host:$PATH" \
CONFIG_SITE="$(pwd)/../config.site" \
../configure \
    --prefix="${PREFIX}" \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-ipv6 \
    --enable-shared \
    --without-ensurepip \
    --with-system-ffi
make PATH="$(pwd)/../build-host:$PATH"
make PATH="$(pwd)/../build-host:$PATH" altinstall
