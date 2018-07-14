import os.path

from .source import URLSource


class Patch:
    def __init__(self, name: str, strip: int = 1) -> None:
        self.name = name
        self.strip = strip

    def apply_file(self, patch, source):
        patch_path = str(patch)
        if not patch.exists():
            patch_path += '.patch'
        source.run_in_source_dir([
            'patch', '--fuzz=0', f'--strip={self.strip}', '--input', patch_path])


class LocalPatch(Patch):
    def apply(self, source):
        self.apply_file(self.package.filesdir / self.name, self.package.source)


class RemotePatch(Patch, URLSource):
    def __init__(self, url: str, *args, **kwargs) -> None:
        self.url = url
        name, _ = os.path.splitext(os.path.basename(url))
        sig_suffix = kwargs.pop('sig_suffix', None)
        Patch.__init__(self, name, *args, **kwargs)
        URLSource.__init__(self, url, sig_suffix=sig_suffix)

    def apply(self, source):
        self.apply_file(self.package.source.src_prefix / self.name, self.package.source)
