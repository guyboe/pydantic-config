# Installation

```bash
pip install --extra-index-url https://test.pypi.org/simple/ pydantic-another-config
```

# Usage

## Create your own settings rules in `settings.py`

```python
import enum
import pathlib
from typing import Union

import pydantic

import pydantic_config


class Settings(pydantic_config.Settings):

    class Config:
        arbitrary_types_allowed = True

    class Input(pydantic.BaseModel):
        device: Union[int, str] = "default"
        samplerate: int

    input: Input = pydantic.Field(default_factory=Input)
    storage: pydantic_config.DirectoryPathCreated = "/tmp/storage"
    source: str
```
Create `settings` directory. You can change it with SETTINGS_PATH environment variable.

Create settings file `settings/default.yaml`

```yaml
input:
    samplerate: 24000
source: source
```

## Validate your settings
```python
import os

import pydantic_config


ENV = os.getenv("ENV", "development")
STAGE = os.getenv("STAGE", "stage")


def main():
    settings = Settings(ENV, STAGE)
    print(settings.dict())


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



class SettingsTypes(str, enum.Enum):
    yaml = "yaml"
    json = "json"
    ini = "ini"


ENV = os.getenv("ENV", "development")
STAGE = os.getenv("STAGE", "stage")


cli = typer.Typer()


@cli.command("settings")
def _settings(
    section: Optional[str] = typer.Option(None),
    format_: ConfigTypes = typer.Option(SettingsTypes.yaml, "--format"),
    output: Optional[pathlib.Path] = typer.Option(None),
    quiet: bool = typer.Option(False),
    indent: int = typer.Option(4)
):
    settings = Settings(ENV, STAGE)
    if output:
        output = output.open("w", encoding="utf-8")
    if section:
        d = benedict(settings).get(section)
    else:
        d = benedict(settings, keypath_separator=None)
    if format_ == SettingsTypes.yaml:
        result = d.to_yaml(allow_unicode="utf-8", indent=indent, default_flow_style=False)
    elif format_ == SettingsTypes.json:
        result = d.to_json(ensure_ascii=False, indent=indent)
    else:
        result = d.to_ini()
    if not quiet:
        print(result, file=output)
```

# Coming soon
