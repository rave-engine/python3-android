#!/usr/bin/env bash
source_manifest="mk/$1/sources.txt"
if [ ! -e "$source_manifest" ] ; then
    exit
fi
source_file=$(cat "$source_manifest")
src_prefix="src/"

if [[ "$source_file" == hg+* || "$source_file" == git+* ]] ; then
    pushd "$src_prefix"
    dest=$(basename "$source_file")
    if [[ "$source_file" == hg+* ]] ; then
        if [ -d "$dest" ] ; then
            cd $dest
            hg pull -u
        else
            hg clone ${source_file:3} "$dest"
        fi
    else
        if [ -d "$dest" ] ; then
            cd $dest
            git fetch --tags origin
            git merge origin/master
        else
            git clone ${source_file:4} "$dest"
        fi
    fi
    popd
else
    wget -N -P "$src_prefix" "$source_file"
fi
