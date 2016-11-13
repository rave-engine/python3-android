# See the wcwidth() test in aclocal.m4. Tested on Android 6.0 and it's broken
./configure \
    bash_cv_wcwidth_broken=yes \
    --prefix=/usr \
    --host="${TARGET}" \
    --build="${HOST}" \
    --disable-shared
make
make install
