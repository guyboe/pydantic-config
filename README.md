# Installation

```bash
pip --extra-index-url https://test.pypi.org/simple/ install pydantic-another-config
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
from pydantic-config import Config


def main():
	config = Config("development", "stage")
	print(config.dict())


if __name__ == "__main__":
	main()
```

# Coming soon
