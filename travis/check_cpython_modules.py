import os.path
import re
import sys

REQUIRED_MODULES = set([
    # Modules with external dependencies
    '_hashlib', '_ssl',             # depends on openssl
    '_curses', '_curses_panel',     # depends on ncurses
    'readline',                     # depends on readline
    '_sqlite3',                     # depends on sqlite
    '_bz2',                         # depends on bzip2
    '_lzma',                        # depends on xz
    '_dbm', '_gdbm',                # depends on gdbm
    '_ctypes', '_ctypes_test',      # depends on libffi
    'zlib',                         # depends on zlib
    # fragile modules
    '_decimal'
])


def main():
    topdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    env = {}
    with open('mk/env.mk', 'rt') as f:
        for line in f:
            key, val = line.strip().split('=', maxsplit=1)
            env[key] = val

    py_configure_ac = os.path.join(topdir, 'src', 'cpython', 'configure.ac')
    with open(py_configure_ac, 'rt') as f:
        for line in f:
            mobj = re.search(r'PYTHON_VERSION,\s*(\d\.\d)', line)
            if mobj:
                pyver = mobj.group(1)
                break

    built_modules = set()
    dynload_dir = os.path.join(env['ANDROID_PREFIX'], env['BUILD_IDENTIFIER'],
                               'usr', 'lib', 'python' + pyver, 'lib-dynload')
    for path, children, nodes in os.walk(dynload_dir):
        for node in nodes:
            name = node.split('.')[0]
            built_modules.add(name)

    missing_modules = REQUIRED_MODULES - built_modules
    if missing_modules:
        print('Missing modules: ' + ', '.join(sorted(list(missing_modules))))
        return 1
    else:
        print('All modules are built')
        return 0


if __name__ == '__main__':
    sys.exit(main())
