import importlib
from .env import packages

dependency = {
    'ncurses': ['autoconf_ncurses'],
    'readline': ['ncurses'],
}

built_packags = set()


def build_package(pkgname: str) -> None:
    if pkgname in built_packags:
        return

    for dep in dependency.get(pkgname, []):
        build_package(dep)

    pkgmod = importlib.import_module(f'pybuild.packages.{pkgname}')
    pkg = getattr(pkgmod, pkgname)

    need_prepare = False

    for src in pkg.sources:
        src.download()
        need_prepare = need_prepare or src.fresh()

    if need_prepare:
        for patch in getattr(pkg, 'patches', []):
            patch.apply()
        try:
            pkg.builder.prepare()
        except NotImplementedError:
            print('Skipping prepare step')

    pkg.builder.build()

    built_packags.add(pkgname)


def main():
    for pkgname in packages:
        build_package(pkgname)
    build_package('python')
