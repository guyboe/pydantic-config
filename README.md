# Installation

```bash
pip install --extra-index-url https://test.pypi.org/simple/ pydantic-another-config
```

# Usage

## Create your own config rules

`config.py`

```python
import enum
import pathlib
from typing import Union

import pydantic

import pydantic_config


class Config(pydantic_config.Settings):

    class Config:
        arbitrary_types_allowed = True

    class Input(pydantic.BaseModel):
        device: Union[int, str] = "default"
        samplerate: int

    input: Input = pydantic.Field(default_factory=Input)
    storage: pydantic.DirectoryPath = "/tmp/storage"
    source: str
```
Create `config` directory. You can change it with CONFIG_PATH environment variable.

Create config file `config/config.yaml`

```yaml
input:
    samplerate: 24000
source: source
```

## Validate your config
```python
import os

from config import Config


ENV = os.getenv("ENV", "development")
STAGE = os.getenv("STAGE", "default")


def main():
    config = Config(ENV, STAGE)
    print(config.dict())


if __name__ == "__main__":
    main()
```

# For example you can use this code for print your config in some formats using typer. Just install `typer` before
```python
import enum
import os
import pathlib
from typing import Optional

from benedict import benedict

import typer

from config import Config


class ConfigTypes(str, enum.Enum):
    yaml = "yaml"
    json = "json"
    ini = "ini"


ENV = os.getenv("ENV", "development")
STAGE = os.getenv("STAGE", "default")


cli = typer.Typer()


@cli.command("config")
def _config(
    section: Optional[str] = typer.Option(None),
    format_: ConfigTypes = typer.Option(ConfigTypes.yaml, "--format"),
    output: Optional[pathlib.Path] = typer.Option(None),
    quiet: bool = typer.Option(False),
    indent: int = typer.Option(4)
):
    config = Config(ENV, STAGE)
    if output:
        output = output.open("w", encoding="utf-8")
    if section:
        d = benedict(config).get(section)
    else:
        d = benedict(config, keypath_separator=None)
    if format_ == "yaml":
        result = d.to_yaml(allow_unicode="utf-8", default_flow_style=False)
    elif format_ == "json":
        result = d.to_json(ensure_ascii=False, indent=indent)
    else:
        result = d.to_ini()
    if not quiet:
        print(result, file=output)
```

# Coming soon
