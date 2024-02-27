import logging

from pathlib import Path

from typing_extensions import Annotated

from pydantic import DirectoryPath
from pydantic.functional_validators import BeforeValidator


def create_directory_path(v):
    Path(v).mkdir(parents=True, exist_ok=True)
    logging.info("Directory %s has been created", v)
    return v


DirectoryPathCreated = Annotated[DirectoryPath, BeforeValidator(create_directory_path)]
