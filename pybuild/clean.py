import argparse
import os
import re
from typing import Iterable

from .package import Package
from .package import enumerate_packages, import_package
from .util import rmtree


def parse_args():
    parser = argparse.ArgumentParser(description='Clean some packages')
    parser.add_argument(
        '--package',
        help='Package name. All packages will be cleaned if not provided.')

    return parser.parse_args()


def parse_packages(pkg_specs: str) -> Iterable[str]:
    for spec in pkg_specs.split(','):
        if spec == ':COMMIT_MARKER':
            if os.getenv('TRAVIS_EVENT_TYPE') == 'cron':
                continue
            mobj = re.search(
                r'pybuild-rebuild=(.+)', os.environ['TRAVIS_COMMIT_MESSAGE'])
            if mobj:
                yield from mobj.group(1).split(',')
        else:
            yield spec


def main():
    args = parse_args()
    if args.package:
        target_packages = [
            import_package(pkg) for pkg in parse_packages(args.package)]
    else:
        target_packages = enumerate_packages()
    for pkg in target_packages:
        for src in pkg.sources:
            src.clean()

    rmtree(Package.BUILDDIR)


if __name__ == '__main__':
    main()
