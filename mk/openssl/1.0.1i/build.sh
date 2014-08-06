pushd src >/dev/null

rm -rf openssl-1.0.1i
tar -xf openssl-1.0.1i.tar.gz || exit 1
pushd openssl-1.0.1i >/dev/null

[[ ! -d "${PREFIX}/share" ]] && (mkdir "${PREFIX}/share" || exit 1)
./Configure dist --prefix="${PREFIX}" --openssldir="${PREFIX}/share" || exit 1
make || exit 1
make install_sw || exit 1

# Remove binaries from premises.
rm -f "${PREFIX}/bin/"{openssl,c_rehash} || exit 1

popd >/dev/null
popd >/dev/null
