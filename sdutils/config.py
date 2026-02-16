from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import os


# Global path for the user configuration file located in the Roaming AppData folder
USER_CONFIG_PATH = Path(os.environ["appdata"], "sdutils.json")


@dataclass
class Config:
    """
    Data container for global application settings.

    Attributes:
        PATH_7D2D: Path to the main '7 Days to Die' installation folder.
        PATH_7D2D_USER: Path to the local user data (Saves, GeneratedWorlds, etc.).
        PATH_7D2D_SERVER: Path to the dedicated server installation (if any).
        PATH_PREFABS: Path to the folder containing custom or vanilla prefabs.
    """
    PATH_7D2D: str | None = None
    PATH_7D2D_USER: str | None = None
    PATH_7D2D_SERVER: str | None = None
    PATH_PREFABS: str | None = None


def _save_config(config: Config, path: Path) -> None:
    """
    Serializes the Config object into a formatted JSON file.

    Args:
        config: The configuration instance to save.
        path: Destination file path.
    """
    json_content = json.dumps(config.__dict__, indent=4)

    with open(path, "w") as writer:
        writer.write(json_content)


def _load_config(path: Path) -> Config:
    """
    Loads configuration settings from a JSON file.

    If the file does not exist, it initializes a default Config object,
    creates the JSON file on disk, and returns the default instance.

    Returns:
        A populated Config instance.
    """
    if not path.exists():
        config = Config()
        _save_config(config, USER_CONFIG_PATH)
        return config

    with open(path, "rb") as reader:
        data = json.load(reader)

    return Config(**data)


# Global singleton instance of the user configuration
try:
    USER_CONFIG = _load_config(USER_CONFIG_PATH)
except Exception as e:
    print(f"Failed loading config at '{USER_CONFIG_PATH}'")
    raise e
