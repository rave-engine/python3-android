from .env import packages
from .package import import_package
from .util import run_in_dir

target_destdir = '/data/local/tmp/python3'


# TODO: don't send unused files (headers, static libraries)


def send_package(pkgname):
    pkg = import_package(pkgname)

    # Most stock Android ROM does not come with a tar that support bz2, so
    # use the uncompressed version
    target_tarball_path = f'/data/local/tmp/{pkg.tarball_name}'
    run_in_dir(['adb', 'shell', 'rm', pkg.tarball_name])
    run_in_dir(['adb', 'push', pkg.tarball_path, target_tarball_path])
    run_in_dir(['adb', 'shell', '/data/local/tmp/busybox', 'tar', 'jxvf', target_tarball_path, '-C', target_destdir])


def main():
    run_in_dir(['adb', 'shell', 'rm', '-rf', target_destdir])
    run_in_dir(['adb', 'shell', 'mkdir', target_destdir])
    for pkgname in packages + ('python',):
        send_package(pkgname)


if __name__ == '__main__':
    main()
