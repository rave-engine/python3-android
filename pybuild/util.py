import os
import pathlib
import shutil
from pathlib import Path
from typing import List, Union

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
    print(f'Removing {path!s}')
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.unlink(path)
    except FileNotFoundError:
        print(f'{path!s} not found, skipping...')
