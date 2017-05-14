import argparse

from .package import Package
from .package import enumerate_packages, import_package
from .util import rmtree


def parse_args():
    parser = argparse.ArgumentParser(description='Clean some packages')
    parser.add_argument(
        '--package',
        help='Package name. All packages will be cleaned if not provided.')

    return parser.parse_args()


def main():
    args = parse_args()
    if args.package:
        target_packages = [import_package(args.package)]
    else:
        target_packages = enumerate_packages()
    for pkg in target_packages:
        for src in pkg.sources:
            src.clean()

    rmtree(Package.BUILDDIR)


if __name__ == '__main__':
    main()
