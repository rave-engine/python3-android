from .package import Package
from .package import enumerate_packages, import_package
from .util import rmtree


def main():
    target_packages = enumerate_packages()
    for pkg in target_packages:
        for src in import_package(pkg).sources:
            src.clean()

    rmtree(Package.BUILDDIR)


if __name__ == '__main__':
    main()
