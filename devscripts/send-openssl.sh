cd src
tar --exclude=.git -zcf openssl.tar.gz openssl/
adb push openssl.tar.gz /sdcard/
rm openssl.tar.gz
