PYTHON3_ROOT=/data/local/tmp/python3

export PATH=$PATH:$PYTHON3_ROOT/usr/bin
if [ ! -z "$LD_LIBRARY_PATH" ] ; then
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:"
fi
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH$PYTHON3_ROOT/usr/lib"
export SSL_CERT_DIR=$PYTHON3_ROOT/etc/ssl/certs
# For ncurses
export TERMINFO=$PYTHON3_ROOT/usr/share/terminfo

export HOME=/data/local/tmp
