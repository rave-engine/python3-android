#!/bin/bash

set -e
set -x

cd build

mkdir -p target/tools
cp ../devscripts/{c_rehash.py,env.sh,import_all.py,ssl_test.py} target/tools

tar cf python3-android.tar target
