import os
import pathlib
import shlex
import shutil
from pathlib import Path
from subprocess import check_call, check_output, run, PIPE
from typing import Any, Dict, List, Union

from .env import target_arch as default_target_arch
from . import arch

BASE = pathlib.Path(__file__).parents[1]

argtype = Union[pathlib.Path, str]


def tostring(value: Union[List[argtype], argtype]) -> str:
    if isinstance(value, list):
        value = ' '.join(map(str, value))
    return str(value)


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
def run_in_dir(cmd: List[str], cwd: Union[str, Path]=None, env: Dict[str, Any]=None, mode='run'):
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
