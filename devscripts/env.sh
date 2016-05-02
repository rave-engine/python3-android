PYTHON3_ROOT=/data/local/tmp/python3

export PATH=$PATH:$PYTHON3_ROOT/bin
if [ ! -z "$LD_LIBRARY_PATH" ] ; then
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:"
fi
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH$PYTHON3_ROOT/lib"
export SSL_CERT_DIR=$PYTHON3_ROOT/share/certs
# For ncurses
export TERMINFO=$PYTHON3_ROOT/share/terminfo
