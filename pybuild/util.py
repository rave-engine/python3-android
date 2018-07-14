import logging
import os
import pathlib
import re
import shlex
import shutil
from pathlib import Path
from subprocess import check_call, check_output, run, PIPE
from typing import Any, Dict, List, Text, Union

from .env import target_arch as default_target_arch, verify_source
from . import arch

BASE = pathlib.Path(__file__).parents[1]

logger = logging.getLogger(__name__)

_PathType = Union[bytes, Text, os.PathLike]


def tostring(value: Union[List[_PathType], _PathType]) -> str:
    if isinstance(value, list):
        value = ' '.join(map(os.fspath, value))
    return os.fspath(value)


def target_arch() -> arch.Arch:
    platform_name = os.getenv('ANDROID_PLATFORM', default_target_arch)
    return getattr(arch, platform_name)()


def rmtree(path: Path) -> None:
    print(f'Removing {os.path.relpath(path)}')
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.unlink(path)
    except FileNotFoundError:
        print(f'{os.path.relpath(path)} not found, skipping...')


# XXX: renamed to run? cwd is no longer required
def run_in_dir(cmd: List[str], cwd: _PathType = None, env: Dict[str, Any] = None, mode='run'):
    if cwd is None:
        cwd = BASE

    print(f'Running in {os.path.relpath(cwd)}: ' + ' '.join([shlex.quote(str(arg)) for arg in cmd]))

    real_env = os.environ.copy()
    if env is not None:
        for key, value in env.items():
            real_env[key] = tostring(value)

    if mode == 'run':
        check_call(cmd, cwd=cwd, env=real_env)
    elif mode == 'result':
        return check_output(cmd, cwd=cwd, env=real_env).decode('utf-8')
    elif mode == 'result_noerror':
        p = run(cmd, stdout=PIPE, stderr=PIPE, cwd=cwd, env=real_env)
        return (b'\n'.join([p.stderr + p.stdout])).decode('utf-8')


class VerificationFailure(Exception):
    pass


def gpg_verify_file(sig_filename, filename, validpgpkeys):
    if not verify_source:
        return

    try:
        import gnupg
    except ImportError:
        logger.error('Failed to import gnupg. Please install python-gnupg or '
                     'set verify_source = False in pybuild/env.py')
        raise SystemExit

    gpg = gnupg.GPG()
    # python-gnupg uses latin-1 by default, which breaks localized date
    # strings in gpg command outputs
    gpg.encoding = 'utf-8'

    with open(filename, 'rb') as f:
        data = f.read()

    verify_result = gpg.verify_data(str(sig_filename), data)
    if verify_result.status not in ('signature good', 'signature valid'):
        raise VerificationFailure(verify_result.status)

    if verify_result.pubkey_fingerprint not in validpgpkeys:
        raise VerificationFailure(f'Signing key {verify_result.pubkey_fingerprint} '
                                  f'not in validpgpkeys {validpgpkeys}')


def gpg_sign_file(filename, key):
    import gnupg

    gpg = gnupg.GPG()
    with open(filename, 'rb') as f:
        sign_result = gpg.sign_file(f, keyid=key, detach=True, binary=False)

    detached_sig = sign_result.data

    with open(str(filename) + '.sig', 'wb') as f:
        f.write(detached_sig)


def parse_ndk_revision(ndk_root):
    with open(ndk_root / 'source.properties', 'r') as f:
        for line in f:
            mobj = re.match(r'Pkg\.Revision\s*=\s*(.+)', line)
            if mobj:
                return mobj.group(1)


def tar_cmd():
    return shutil.which('gnutar') or shutil.which('tar')
