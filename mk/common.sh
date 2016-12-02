source_manifest() {
    echo "${BASE}/mk/$1/sources.json"
}
source_url() {
    jq -r ".[0].url" "$(source_manifest $1)"
}

source_filename() {
    basename $(source_url $1)
}

source_protocol() {
    jq -r ".[0].protocol" "$(source_manifest $1)"
}

get_source_folder() {
    source_alias=$(jq -r ".[0].alias" "$(source_manifest $1)")
    if [[ "$source_alias" != "null" ]] ; then
        echo "$source_alias"
        return
    fi

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
    protocol="$(source_protocol $NAME)"
    pushd "${BASE}/src"

    source_folder="$(get_source_folder $NAME)"
    if [[ ! -e "$source_folder" ]] ; then
        return
    fi

    if [[ "$protocol" == hg ]] ; then
        pushd "$source_folder"
        hg revert --all
        hg purge --all
        popd
    elif [[ "$protocol" == git ]] ; then
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
