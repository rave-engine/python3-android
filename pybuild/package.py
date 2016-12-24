import pathlib

from .util import BASE


class Package:
    def __init__(self, name: str):
        self.name = name

    @property
    def filesdir(self) -> pathlib.Path:
        return BASE / 'mk' / self.name
