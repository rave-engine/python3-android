import yaml

data = {
    'image': 'yan12125/python3-android-base:latest',
}

# use a separate object so that PyYAML uses anchors
scripts = [
    './devscripts/import_pgp_keys.sh',
    'make',
    'make test',
]

for arch in ('arm', 'arm64', 'x86', 'x86_64'):
    for api in (21, 29):
        data[f'build_{arch}_api_{api}'] = {
            'variables': {
                'ANDROID_PLATFORM': arch,
                'ANDROID_API_LEVEL': api,
            },
            'script': scripts,
        }


class MyDumper(yaml.SafeDumper):
    # HACK: override anchor names given by serializers
    def generate_anchor(self, node):
        return 'scripts'

    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


with open('.gitlab-ci.yml', 'w') as f:
    yaml.dump(data, Dumper=MyDumper, stream=f, sort_keys=False)
