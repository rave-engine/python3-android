pushd src/cpython || exit 1

hg revert --all
hg purge --all

if test "$PYTHON_HOST_BUILD" = "yes" ; then
    # Build host components.
    mkdir build-host && pushd build-host
    AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib ../configure || exit 1
    AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib make || exit 1
    popd
fi

# Apply patches and build target Python.
cat > config.site <<-SITE
	ac_cv_file__dev_ptmx=no
	ac_cv_file__dev_ptc=no
SITE

patch -p1  < "${FILESDIR}/cross-compile.patch" || exit 1
patch -p1  < "${FILESDIR}/python-misc.patch" || exit 1
patch -p1  < "${FILESDIR}/android-misc.patch" || exit 1
patch -p1  < "${FILESDIR}/soundcard-h-path.patch" || exit 1
patch -p1  < "${FILESDIR}/android-l-pie.patch" || exit 1
patch -p1  < "${FILESDIR}/passwd-pw_gecos.patch" || exit 1
patch -p1  < "${FILESDIR}/ndk-android-support.patch" || exit 1
patch -p1  < "${FILESDIR}/allow-disable-libmpdec.patch" || exit 1

autoreconf --install --verbose --force

mkdir build-target && pushd build-target
../configure CPPFLAGS="${CPPFLAGS} -I${PREFIX}/include/android-support" HOSTPYTHON="$(pwd)/../build-host/python" CONFIG_SITE="$(pwd)/../config.site" --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-ipv6 --enable-shared --without-ensurepip --with-android-support --without-decimal-module || exit 1
make HOSTPYTHON="$(pwd)/../build-host/python" || exit 1
make HOSTPYTHON="$(pwd)/../build-host/python" altinstall || exit 1

popd >/dev/null
