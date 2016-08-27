source_url() {
    head -n 1 "${BASE}/mk/$1/sources.txt"
}

source_filename() {
    basename $(source_url $1)
}

get_source_folder() {
    filename=$(source_filename $1)
    if [[ "$filename" == *.tar.* ]] ; then
        echo "${filename%.tar.*}"
    elif [[ "$filename" == *.tgz ]] ; then
        echo "${filename%.tgz}"
    else
        echo "$filename"
    fi
}

clean_package() {
    local NAME=$1

    url="$(source_url $NAME)"
    pushd "${BASE}/src"

    source_folder="$(get_source_folder $NAME)"
    if [[ ! -e "$source_folder" ]] ; then
        return
    fi

    if [[ "$url" == hg+* ]] ; then
        pushd "$source_folder"
        hg revert --all
        hg purge --all
        popd
    elif [[ "$url" == git+* ]] ; then
        pushd "$source_folder"
        git checkout .
        git clean -dfx
        popd
    else
        rm -rvf "$source_folder"
    fi
    popd
}

clean_and_extract_package() {
    local NAME=$1

    clean_package $NAME

    filename=$(source_filename $NAME)
    echo $filename
    if [[ "$filename" == *.tar.* || "$filename" == *.tgz ]] ; then
        pushd "${BASE}/src"
        tar -xvf "$(source_filename $NAME)"
        popd
    fi
}
