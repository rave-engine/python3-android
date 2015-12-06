#!/usr/bin/env bash
source_manifest="mk/$1/$2/sources.txt"
source_file=$(cat "$source_manifest")
src_prefix="src/"

if [[ "$source_file" == hg+* ]] ; then
    pushd "$src_prefix"
    dest=$(basename "$source_file")
    if [ -d "$dest" ] ; then
        cd $dest
        hg pull -u
    else
        hg clone ${source_file:3} "$dest"
    fi
    popd
else
    wget -N -P "$src_prefix" "$source_file"
fi
