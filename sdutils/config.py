from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import os


USER_CONFIG_PATH = Path(os.environ["appdata"], "sdutils.json")


@dataclass
class Config:
    PATH_7D2D: str | None = None
    PATH_7D2D_USER: str | None = None
    PATH_7D2D_SERVER: str | None = None
    PATH_PREFABS: str | None = None


def _save_config(config: Config, path: Path) -> None:

    json_content = json.dumps(config.__dict__, indent=4)

    with open(path, "w") as writer:
        writer.write(json_content)


def _load_config(path: Path) -> Config:
    """
    Load a config object stored in a json file
    """
    if not path.exists():
        config = Config()
        _save_config(config, USER_CONFIG_PATH)
        return config

    with open(path, "rb") as reader:
        data = json.load(reader)

    return Config(**data)


try:
    USER_CONFIG = _load_config(USER_CONFIG_PATH)
except Exception as e:
    print(f"Failed loading config at '{USER_CONFIG_PATH}'")
    raise e
