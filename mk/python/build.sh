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
patch -p1  < "${FILESDIR}/android-l-pie.patch" || exit 1

autoreconf --install --verbose --force

mkdir build-target && pushd build-target
../configure PATH="$(pwd)/../build-host:$PATH" CONFIG_SITE="$(pwd)/../config.site" --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-ipv6 --enable-shared --without-ensurepip || exit 1
make PATH="$(pwd)/../build-host:$PATH" || exit 1
make PATH="$(pwd)/../build-host:$PATH" altinstall || exit 1

popd >/dev/null
