import logging
import pathlib
import sys

from nvchecker_toolbelt import check_pkgs

from pybuild.package import import_package

ROOT = pathlib.Path(__file__).parent.resolve()


class PyBuildHandler:
    SCRIPT_NAME = 'pybuild'

    def get_version(self, pkgname):
        pkg = import_package(pkgname)
        return pkg.version


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sys.exit(check_pkgs(PyBuildHandler()))
