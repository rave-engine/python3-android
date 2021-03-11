export PATH=$PATH:$PWD/usr/bin
if [ ! -z "$LD_LIBRARY_PATH" ] ; then
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:"
fi
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH$PWD/usr/lib"
export SSL_CERT_FILE="$PWD/etc/ssl/cert.pem"
# For ncurses
export TERMINFO="$PWD/usr/share/terminfo"

export HOME=/data/local/tmp
