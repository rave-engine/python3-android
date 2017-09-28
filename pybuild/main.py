import os
import re
from typing import Iterable

from .env import use_bintray
from .package import enumerate_packages, import_package

built_packags: set = set()
need_rebuild: set = set()


def parse_packages(pkg_specs: str) -> Iterable[str]:
    for spec in pkg_specs.split(','):
        if spec == ':COMMIT_MARKER':
            if os.getenv('TRAVIS_EVENT_TYPE') == 'cron':
                continue
            mobj = re.search(
                r'pybuild-rebuild=(.+)', os.getenv('TRAVIS_COMMIT_MESSAGE', ''))
            if mobj:
                pkgs = mobj.group(1)
                if pkgs == 'ALL':
                    yield from enumerate_packages()
                else:
                    yield from pkgs.split(',')
        else:
            yield spec


def build_package(pkgname: str) -> None:
    if pkgname in built_packags:
        return

    pkg = import_package(pkgname)

    if use_bintray and pkgname not in need_rebuild and pkg.fetch_tarball():
        built_packags.add(pkgname)
        return

    for dep in pkg.dependencies:
        build_package(dep)

    if pkg.fresh():
        for src in pkg.sources:
            src.download()

        for patch in getattr(pkg, 'patches', []):
            patch.apply(pkg.source)
        try:
            pkg.prepare()
        except NotImplementedError:
            print('Skipping prepare step')

    pkg.build()

    pkg.create_tarball()
    pkg.upload_tarball()

    built_packags.add(pkgname)


def main():
    # TODO: Make this configurable
    need_rebuild.update(parse_packages(':COMMIT_MARKER'))
    print(f'Packages to rebuild: {need_rebuild}')
    build_package('python')
