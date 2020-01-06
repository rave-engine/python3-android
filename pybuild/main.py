import logging

from .package import import_package

built_packags: set = set()


logger = logging.getLogger(__name__)


def build_package(pkgname: str) -> None:
    if pkgname in built_packags:
        return

    pkg = import_package(pkgname)

    logger.info(f'Building {pkgname} {pkg.get_version()}')

    if pkg.need_download():
        for src in pkg.sources:
            src.download()

        # All signatures should be downloaded first so that sources can be verified
        for src in pkg.sources:
            src.verify(pkg.validpgpkeys)
            src.extract()

        for patch in getattr(pkg, 'patches', []):
            patch.apply(pkg.source, pkg)

    for dep in pkg.dependencies:
        build_package(dep)

    pkg.build()

    built_packags.add(pkgname)


def main():
    logging.basicConfig(level=logging.DEBUG)

    build_package('python')
