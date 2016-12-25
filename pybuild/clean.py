from .builder import Builder
from .package import enumerate_packages
from .util import rmtree


def main():
    for pkg in enumerate_packages():
        for src in pkg.sources:
            src.clean()

    rmtree(Builder.BUILDDIR)


if __name__ == '__main__':
    main()
