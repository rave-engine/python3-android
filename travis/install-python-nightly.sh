if [[ "$(uname)" == "Linux" ]] ; then
    wget https://s3.amazonaws.com/travis-python-archives/binaries/ubuntu/14.04/x86_64/python-nightly.tar.bz2
    sudo tar -jxf python-nightly.tar.bz2 --directory /
    export PATH="$PATH:/opt/python/3.7-dev/bin"
else
    brew install --HEAD --without-readline --without-xz --without-gdbm --without-sqlite python3
fi
