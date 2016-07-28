source_url() {
    head -n 1 "${BASE}/mk/$1/sources.txt"
}

source_filename() {
    basename $(source_url $1)
}

source_folder() {
    filename=$(source_filename $1)
    echo "${filename%.tar.*}"
}

clean_package() {
    local NAME=$1

    url="$(source_url $NAME)"
    pushd "${BASE}/src"
    if [[ "$url" == hg+* ]] ; then
        pushd "$(source_folder $NAME)"
        hg revert --all
        hg purge --all
        popd
    elif [[ "$url" == git+* ]] ; then
        pushd "$(source_folder $NAME)"
        git checkout .
        git clean -dfx
        popd
    else
        rm -rvf "$(source_folder $NAME)"
    fi
    popd
}

clean_and_extract_package() {
    local NAME=$1

    clean_package $NAME

    filename=$(source_filename $NAME)
    echo $filename
    if [[ "$filename" == *.tar.* ]] ; then
        pushd "${BASE}/src"
        tar -xvf "$(source_filename $NAME)"
    fi
}
