import os
import enum
import pathlib
import itertools
import importlib

from typing import Dict, Any, Callable

import pydantic

from benedict import benedict

from . import validators


DEFAULT = "default"
FINAL = "final"

ENV_PREFIX = os.environ.get("ENV_PREFIX", "")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "config")
ENV_NESTED_DELIMITER = os.environ.get("ENV_NESTED_DELIMITER", "__")


def resolve_filepath(value):
    path = pathlib.Path(value)
    if path.is_file():
        return str(path.resolve())
    raise ValueError("Value must be a path to file and exists")


class Url(pydantic.AnyUrl):
    host_required: bool = False


try:
    from enum import StrEnum  # pylint: disable=no-name-in-module,unused-import
except:  # pylint: disable=bare-except
    class StrEnum(enum.Enum):
        @staticmethod
        def _generate_next_value_(name, *_):
            return name.lower()


def _file_settings(filename: str) -> Callable:

    path = (pathlib.Path(CONFIG_PATH) / pathlib.Path(filename)).resolve()

    def func(_: pydantic.BaseSettings) -> Dict[str, Any]:
        if not path.exists():
            return {}
        if path.suffix in importlib.machinery.SOURCE_SUFFIXES:
            modulename = ".".join(
                path.relative_to(pathlib.Path.cwd()).with_suffix("").parts
            )
            data = {}
            module = importlib.import_module(modulename)
            for var in module.__all__:
                data.update({var: getattr(module, var)})
        else:
            data = benedict(str(path), keypath_separator=None)
        return data

    return func


class Settings(pydantic.BaseSettings):

    # ---- Settings config
    class Config:

        env_prefix = ENV_PREFIX
        env_nested_delimiter = ENV_NESTED_DELIMITER

        @classmethod
        def customise_sources(
            cls, init_settings, env_settings, file_secret_settings,
        ):
            return (init_settings,) \
                + (env_settings,) \
                + tuple(_file_settings(filename) for filename in reversed(cls.SOURCES)) \
                + (file_secret_settings,)

    # ---- Global settings fields
    env: str
    stage: str
    debug: bool = False

    def __new__(cls, env, stage, **_):
        cls.Config.SOURCES = [k + v for k, v in itertools.product(
            [DEFAULT, env, stage, FINAL],
            [".yml", ".yaml", ".json"] + importlib.machinery.SOURCE_SUFFIXES
        )]
        return super().__new__(cls)  # pylint: disable=no-value-for-parameter

    def __init__(self, env, stage, **kwargs):
        super().__init__(**{"env": env, "stage": stage, **kwargs})
