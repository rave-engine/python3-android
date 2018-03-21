from .package import enumerate_packages, import_package


def main():
    target_packages = enumerate_packages()
    for pkgname in target_packages:
        pkg = import_package(pkgname)
        if hasattr(pkg, 'validpgpkeys'):
            print('\n'.join(pkg.validpgpkeys))


if __name__ == '__main__':
    main()
