pushd src/cpython >/dev/null

hg revert --all
hg purge --all

# Build host components.
mkdir build-host && pushd build-host
AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib ../configure || exit 1
AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib make || exit 1
popd

# Apply patches and build target Python.
cat > config.site <<-SITE
	ac_cv_file__dev_ptmx=no
	ac_cv_file__dev_ptc=no
SITE

patch -p1  < "${FILESDIR}/${PACKAGE}-cross-compile.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-python-misc.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-android-locale.patch" || exit 1
patch -Ep1 < "${FILESDIR}/${PACKAGE}-android-libmpdec.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-android-misc.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-modules-link-libm.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-soundcard-h-path.patch" || exit 1

autoreconf --install --verbose

mkdir build-target && pushd build-target
../configure CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/../build-host/python" CONFIG_SITE="$(pwd)/../config.site" --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-ipv6 --enable-shared --without-ensurepip || exit 1
make CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/../build-host/python" HOSTPGEN="$(pwd)/../build-host/Parser/pgen" || exit 1
make CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/../build-host/python" HOSTPGEN="$(pwd)/../build-host/Parser/pgen" install || exit 1

popd >/dev/null
