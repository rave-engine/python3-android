#!/bin/bash

set -e
set -x

source ./env

NAME=${BUILD_IDENTIFIER}

cd build

mkdir -p $NAME/tools
cp ../devscripts/{c_rehash.py,env.sh,import_all.py} $NAME/tools

tar cf ${NAME}.tar $NAME
