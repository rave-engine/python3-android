from .source import Source
from .util import BASE


class Patch:
    def __init__(self, source: Source, name: str, strip=1):
        self.source = source
        self.name = name
        self.strip = strip

    def apply_file(self, patch):
        patch_path = str(patch)
        if not patch.exists():
            patch_path += '.patch'
        self.source.run_in_source_dir([
            'patch', '--fuzz=0', f'--strip={self.strip}', '--input', patch_path])


class LocalPatch(Patch):
    def apply(self):
        self.apply_file(self.source.package.filesdir / self.name)


class RemotePatch(Patch):
    def apply(self):
        self.apply_file(BASE / Source.src_prefix / self.name)
