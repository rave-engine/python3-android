import os.path


class Patch:
    def __init__(self, name: str, strip: int=1) -> None:
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


class RemotePatch(Patch):
    def __init__(self, url: str, *args, **kwargs) -> None:
        self.url = url
        name, _ = os.path.splitext(os.path.basename(url))
        super(RemotePatch, self).__init__(name, *args, **kwargs)

    def apply(self, source):
        self.apply_file(self.package.source.src_prefix / self.name, self.package.source)
