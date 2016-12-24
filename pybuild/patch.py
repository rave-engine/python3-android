from .source import Source
from .util import BASE


class Patch:
    def __init__(self, source: Source, name: str):
        self.source = source
        self.name = name

    def apply_file(self, patch):
        self.source.run_in_source_dir([
            'patch', '--fuzz=0', '--strip=1', '--input', patch])


class LocalPatch(Patch):
    def apply(self):
        self.apply_file(self.source.package.filesdir / f'{self.name}.patch')


class RemotePatch(Patch):
    def apply(self):
        self.apply_file(BASE / Source.src_prefix / f'{self.name}.patch')
