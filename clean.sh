[ -d src/cpython ] && pushd src/cpython && git clean -dfx && git checkout && popd
rm -rf build
