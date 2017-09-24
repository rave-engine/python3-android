from .env import packages
from .package import import_package

built_packags: set = set()


def build_package(pkgname: str) -> None:
    if pkgname in built_packags:
        return

    pkg = import_package(pkgname)

    if pkg.fetch_tarball():
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
    for pkgname in packages:
        build_package(pkgname)
    build_package('python')
