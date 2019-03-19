pushd src >/dev/null

rm -rf "Python-${VERSION}"
tar -xf "Python-${VERSION}.tar.xz" || exit 1
pushd "Python-${VERSION}" >/dev/null

# Build host components.
#AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib ./configure || exit 1
#AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib make BUILDPYTHON=hostpython hostpython PGEN=Parser/hostpgen Parser/hostpgen || exit 1

echo "Step 2"
echo "Toold Prefix is ${TOOL_PREFIX}. Linux is {linux,sys}"
#AR=ar AS=as CC=clang CFLAGS= CPP="clang -E" CPPFLAGS= CXX=clang++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib make BUILDPYTHON=hostpython hostpython PGEN=Parser/hostpgen Parser/hostpgen || exit 1
#$AR="${AR}" AS="${AS}" CC="${CC}" CFLAGS="${CFLAGS}" CPP="${CPP}" CPPFLAGS="${CPPFLAGS}" CXX="${CXX}" CXXFLAGS="${CXXFLAGS}" LD="${LD}" LDFLAGS="${LDFLAGS}" RANLIB="${RANLIB}" make BUILDPYTHON=hostpython hostpython PGEN=Parser/hostpgen Parser/hostpgen || exit 1


autoreconf --install --verbose --force


####  BDS START
#$$$AR="${AR}" AS="${AS}" CC="${CC}" CFLAGS="${CFLAGS}" CPP="${CPP}" CPPFLAGS="${CPPFLAGS}" CXX="${CXX}" CXXFLAGS="${CXXFLAGS}" LD="${LD}" LDFLAGS="${LDFLAGS}" RANLIB="${RANLIB}" ./configure || exit 1

#$AR="${AR}" AS="${AS}" CC="${CC}" CFLAGS= CPP="${CPP}" CPPFLAGS= CXX="${CXX}" CXXFLAGS= LD="${LD}" LDFLAGS= RANLIB="${RANLIB}" ./configure || exit 1
##AR=ar AS=as CC=clang CFLAGS= CPP="clang -E" CPPFLAGS= CXX=clang++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib ./configure || exit 1
##./configure --without-gcc --host="${TARGET}" --build="${HOST}" --disable-ipv6 CONFIG_SITE=config.site || exit 1
###RANLIB="${RANLIB}" ./configure || exit 1
echo "Step 2.1"
##AR=ar AS=as CC=clang CFLAGS= CPP="clang -E" CPPFLAGS= CXX=clang++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib make BUILDPYTHON=hostpython hostpython PGEN=Parser/hostpgen Parser/hostpgen || exit 1
#$$make BUILDPYTHON=hostpython hostpython PGEN=Parser/hostpgen Parser/hostpgen || exit 1
#AR=ar AS=as CC=gcc CFLAGS= CPP=cpp CPPFLAGS= CXX=g++ CXXFLAGS= LD=ld LDFLAGS= RANLIB=ranlib make BUILDPYTHON=hostpython hostpython PGEN=Parser/hostpgen Parser/hostpgen || exit 1
####  BDS END


echo "Step 3"
###make distclean || exit 1

echo "Step 4"

# Apply patches and build target Python.
cat > config.site <<-SITE
	ac_cv_file__dev_ptmx=no
	ac_cv_file__dev_ptc=no
SITE
#ln -sf "${TOOL_PREFIX}/sysroot/usr/include/"{linux,sys}"/soundcard.h"
patch -p1  < "${FILESDIR}/${PACKAGE}-setup.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-cross-compile.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-python-misc.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-android-locale.patch" || exit 1
patch -Ep1 < "${FILESDIR}/${PACKAGE}-android-libmpdec.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-android-misc.patch" || exit 1
#patch -p1  < "${FILESDIR}/${PACKAGE}-android-print.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-android-extras.patch" || exit 1
#patch -p1  < "${FILESDIR}/${PACKAGE}-accept4.patch" || exit 1
patch -p1  < "${FILESDIR}/${PACKAGE}-python-nl_langinfo.patch" || exit 1 
patch -p1  < "${FILESDIR}/${PACKAGE}-android-audio.patch" || exit 1 


#./configure CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/hostpython" CONFIG_SITE=config.site --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-ipv6 --enable-shared --without-ensurepip || exit 1 
echo "Step 5"
./configure CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/hostpython" CONFIG_SITE=config.site --prefix="${PREFIX}" --host="${TARGET}" --build="${HOST}" --disable-ipv6 --enable-shared --without-ensurepip --with-system-ffi --with-system-expat || exit 1 
# ./configure CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/hostpython" CONFIG_SITE=config.site \
#      --prefix="${PREFIX}" \
#      --host="${TARGET}" \
#      --build="${HOST}" \
#      --disable-ipv6 \
# #     --target="${TARGET}" \
# ##     --enable-shared \
# #     --with-system-ffi \
# #     --with-system-expat \
# ##     --without-ensurepip \
#      || exit 1

echo "Step 6"

make CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/hostpython" HOSTPGEN="$(pwd)/Parser/hostpgen" || exit 1
make CROSS_COMPILE_TARGET=yes HOSTPYTHON="$(pwd)/hostpython" HOSTPGEN="$(pwd)/Parser/hostpgen" install || exit 1

popd >/dev/null
popd >/dev/null

echo "Step 7"