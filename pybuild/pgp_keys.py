import itertools
import logging
import tempfile

import gnupg

from .env import gpg_key_id
from .package import enumerate_packages, import_package
from .util import BASE

GPG_SERVER = 'pool.sks-keyservers.net'


def main():
    logging.basicConfig(level=logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdir:
        gpg = gnupg.GPG(gnupghome=tmpdir)
        gpg.encoding = 'utf-8'

        keys_map = {}

        target_packages = enumerate_packages()
        for pkgname in target_packages:
            pkg = import_package(pkgname)
            keys_map[pkgname] = getattr(pkg, 'validpgpkeys', [])

        # Also fetch my signing key for prebuilt archives
        keys_map['yan12125'] = [gpg_key_id]

        result = gpg.recv_keys(GPG_SERVER, *list(itertools.chain.from_iterable(keys_map.values())))
        assert result

        pgp_keys_dir = BASE / 'devscripts' / 'pgp-keys'
        for name, key_ids in keys_map.items():
            exported_keys = ''
            for key in key_ids:
                current_key = gpg.export_keys([key], armor=True)
                exported_keys += current_key

            if exported_keys:
                with open(pgp_keys_dir / (name + '.asc'), 'w') as f:
                    f.write(exported_keys)


if __name__ == '__main__':
    main()
