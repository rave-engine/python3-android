import importlib
import os.path
import pathlib
from typing import Iterator

from .util import BASE


class Package:
    def __init__(self, name: str):
        self.name = name

    @property
    def filesdir(self) -> pathlib.Path:
        return BASE / 'mk' / self.name


def import_package(pkgname: str) -> Package:
    pkgmod = importlib.import_module(f'pybuild.packages.{pkgname}')
    return getattr(pkgmod, pkgname)


def enumerate_packages() -> Iterator[Package]:
    for child in (pathlib.Path(__file__).parent / 'packages').iterdir():
        pkgname, ext = os.path.splitext(os.path.basename(child))
        if ext != '.py':
            continue
        yield import_package(pkgname)
