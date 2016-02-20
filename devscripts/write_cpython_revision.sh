#!/usr/bin/env bash
cd src/cpython || exit 1
hg parents -T "{rev}:{node|short}\n" > ../../mk/python/LAST_WORKING_REVISION
