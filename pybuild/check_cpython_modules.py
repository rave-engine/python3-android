import os.path
import re
import sys

from .package import import_package, Package

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
    'pyexpat',                      # depends on expat
    # fragile modules
    '_decimal'
])

PROHIBITED_MODULES = set([
    # Modules that are not applicable on Android
    '_crypt',                       # Android does not have crypt()
    'grp',                          # Android does not have getgrent()
])


def main():
    py_configure_ac = import_package('python').source.source_dir / 'configure.ac'
    with open(py_configure_ac, 'rt') as f:
        for line in f:
            mobj = re.search(r'PYTHON_VERSION,\s*(\d\.\d)', line)
            if mobj:
                pyver = mobj.group(1)
                break

    built_modules = set()
    dynload_dir = Package.BUILDDIR / 'target' / 'python' / 'usr' / 'lib' / f'python{pyver}' / 'lib-dynload'
    for path, children, nodes in os.walk(dynload_dir):
        for node in nodes:
            name = node.split('.')[0]
            built_modules.add(name)

    result = 0
    missing_modules = REQUIRED_MODULES - built_modules
    if missing_modules:
        print('Missing modules: ' + ', '.join(sorted(list(missing_modules))))
        result = 1
    else:
        print('All modules are built')

    evil_modules = built_modules & PROHIBITED_MODULES
    if evil_modules:
        print('Found unexpected modules: ' + ', '.join(sorted(list(evil_modules))))
        result = 1
    else:
        print('No unexpected modules found')

    return result


if __name__ == '__main__':
    sys.exit(main())
