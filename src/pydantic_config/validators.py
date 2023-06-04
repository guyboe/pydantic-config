import pathlib
import logging


def create_directory_path(v):
    pathlib.Path(v).mkdir(parents=True, exist_ok=True)
    logging.info("Directory %s has been created", v)
    return v
