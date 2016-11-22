import os
from os.path import abspath, dirname, exists, join
import subprocess
import sys

ssl_cert_src = '/system/etc/security/cacerts'
# This file is installed at $PREFIX/tools/
ssl_cert_dst = join(dirname(dirname(abspath(__file__))), 'etc', 'ssl', 'certs')

if len(sys.argv) == 3:
    ssl_cert_src = sys.argv[1]
    ssl_cert_dst = sys.argv[2]

for cert in os.listdir(ssl_cert_src):
    old_path = join(ssl_cert_src, cert)
    new_hash = subprocess.check_output([
        'openssl', 'x509', '-noout', '-hash', '-in', old_path
    ]).strip().decode('ascii')
    for index in range(10):
        new_path = join(ssl_cert_dst, '%s.%s' % (new_hash, index))
        if not exists(new_path):
            break
    print('%s => %s' % (old_path, new_path))
    os.symlink(old_path, new_path)
