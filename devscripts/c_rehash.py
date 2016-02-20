import os
import os.path
import subprocess
import sys

SSL_CERT_SRC = sys.argv[1]
SSL_CERT_DST = sys.argv[2]

for cert in os.listdir(SSL_CERT_SRC):
    old_path = os.path.join(SSL_CERT_SRC, cert)
    new_hash = subprocess.check_output([
        'openssl', 'x509', '-noout', '-hash', '-in', old_path
    ]).strip().decode('ascii')
    for index in range(10):
        new_path = os.path.join(SSL_CERT_DST, '%s.%s' % (new_hash, index))
        if not os.path.exists(new_path):
            break
    print('%s => %s' % (old_path, new_path))
    os.symlink(old_path, new_path)
