for i in {001..008} ; do
    patch -F0 -p0 -i "${BASE}/src/readline63-$i"
done
