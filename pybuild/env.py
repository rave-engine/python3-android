target_arch = 'arm64'
android_api_level = 21

# Python optional modules.
# Available:
#  bzip2 - enable the bz2 module and the bzip2 codec
#  xz - enable the lzma module and the lzma codec
#  openssl - enable the ssl module and SSL/TLS support for sockets
#  readline - enable the readline module and command history/the like in the REPL
#  ncurses - enable the curses module
#  sqlite - enable the sqlite3 module
#  gdbm - enable the dbm/gdbm modules
#  libffi - enable the ctypes module
#  zlib - enable the zlib module
#  expat - enable the pyexpat module
#  tools - some handy utility scripts from ./devscripts
packages = ('strace', 'openssl', 'ncurses', 'readline', 'sqlite', 'bzip2', 'xz', 'gdbm', 'libffi', 'zlib', 'expat', 'tools')

# Enable GPG signature verification on source tarballs and patches?
verify_source = True

# The GPG key to sign prebuilt archives
# Don't change this unless you're going to distribute your archives!
gpg_key_id = '481C4474AF1572165AE4C6AF3FDDD575826C5C30'
