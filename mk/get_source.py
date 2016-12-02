#!/usr/bin/env python

import json
import os.path
import sys
from subprocess import check_call

source_manifest = 'mk/%s/sources.json' % sys.argv[1]
if not os.path.exists(source_manifest):
    sys.exit(1)

src_prefix = 'src'

with open(source_manifest, 'rt') as f:
    sources = json.loads(f.read())
    for source in sources:
        # Python's basename does not strip /
        source_url = source['url'].strip('/')
        protocol = source.get('protocol')
        dest = source.get('alias', os.path.basename(source_url))
        cwd = os.path.join(src_prefix, dest)
        already_cloned = os.path.isdir(os.path.join(src_prefix, dest))
        if protocol == 'hg':
            if already_cloned:
                check_call(['hg', 'pull', '-u'], cwd=cwd)
            else:
                check_call(['hg', 'clone', source_url, dest], cwd=src_prefix)
        elif protocol == 'git':
            if already_cloned:
                check_call(['git', 'fetch', '--tags', 'origin'], cwd=cwd)
                check_call(['git', 'merge', 'origin/master'], cwd=cwd)
            else:
                check_call(['git', 'clone', source_url, dest], cwd=src_prefix)
        else:
            check_call(['wget', '--continue', '--timestamping',
                                '--directory-prefix', src_prefix, source_url])
