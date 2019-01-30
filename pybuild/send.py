import os.path

from .package import Package
from .util import run_in_dir

target_destdir = '/data/local/tmp/python3'


# TODO: don't send unused files (headers, static libraries)


def send_package(pkgname):
    target_tarball_path = '/data/local/tmp/python3-android.tar.bz2'
    target_tarball_name = os.path.basename(target_tarball_path)
    run_in_dir(['tar', 'jcvf', target_tarball_name, 'sysroot'], cwd=Package.SYSROOT.parent)
    run_in_dir(['adb', 'push', str(Package.SYSROOT.parent / target_tarball_name), target_tarball_path])


def main():
    run_in_dir(['adb', 'shell', 'rm', '-rf', target_destdir])
    run_in_dir(['adb', 'shell', 'mkdir', target_destdir])
    send_package('python')


if __name__ == '__main__':
    main()
