from typing import List
from pathlib import Path
from re import Match
import subprocess
import shutil
import os
import re

import click


MOD_NAME_PROP = "@MODNAME"


def _multi_split(string: str) -> List[str]:
    """
    Splits a string into words by replacing any non-alphanumeric character
    with a dash and splitting by that dash.
    """
    return re.sub(r"\W+", repl="-", string=string).split("-")


def _format_pascal(value: str) -> str:
    """
    Formats a string into PascalCase (e.g., 'my-mod' -> 'MyMod').
    """
    words = [word.capitalize() for word in _multi_split(value)]
    return "".join(words)


def _format_camel(value: str) -> str:
    """
    Formats a string into camelCase (e.g., 'my-mod' -> 'myMod').
    """
    result = _format_pascal(value)

    return result[0].lower() + result[1:]


def _format_snake(value: str) -> str:
    """
    Formats a string into snake_case (e.g., 'my-mod' -> 'my_mod').
    """
    words = [word.lower() for word in _multi_split(value)]
    return "_".join(words)


def _format_kebab(value: str) -> str:
    """
    Formats a string into kebab-case (e.g., 'MyMod' -> 'my-mod').
    """
    words = [word.lower() for word in _multi_split(value)]
    return "-".join(words)


def _render_placeholder(match: Match, value: str) -> str:
    """
    Determines the correct formatting for a placeholder match based on
    the optional format flag (e.g., @MODNAME!pascal).

    Args:
        match: The regex match object containing groups for the key and format.
        value: The raw value to be formatted (the mod name).

    Returns:
        The formatted string.
    """
    format = match.groups()[1]

    if format is None:
        return value

    match format:
        case "!pascal":
            return _format_pascal(value)

        case "!camel":
            return _format_camel(value)

        case "!snake":
            return _format_snake(value)

        case "!kebab":
            return _format_kebab(value)

    raise ValueError(f"Invalid format: '{format}'")


def _render_placeholders(content: str, datas: dict) -> str:
    """
    Parses a string and replaces all occurrences of registered placeholders
    with their corresponding formatted values.
    """
    for key, value in datas.items():

        content = re.sub(
            pattern=f"({key})(!\\w+)?",
            repl=lambda match: _render_placeholder(match, value),
            string=content,
        )

    return content


def _render_template(filename: Path, datas: dict):
    """
    Opens a file, processes its template placeholders, and overwrites it
    with the rendered content.
    """
    with open(filename, "r") as reader:
        content = reader.read()

    content = _render_placeholders(content, datas)

    with open(filename, "w") as writer:
        writer.write(content)


@click.command("new")
@click.argument("mod-name")
def cmd_new(mod_name: str):
    """
    Creates a new 7D2D Modding project from templates.

    This command generates a standard folder structure, copies template files
    (ModInfo, C# project, Gitignore), renders placeholders with the chosen
    mod name, and initializes a Git repository.
    """
    PLACEHOLDERS = {MOD_NAME_PROP: mod_name}

    templates_dir = Path(__file__, "../../templates").resolve()

    if Path(mod_name).exists():
        raise SystemExit(f"Error: A folder with name '{mod_name}' already exists")

    csproj = f"{_format_kebab(mod_name)}.csproj"

    # Directory Structure Creation
    os.makedirs(mod_name)
    os.makedirs(Path(mod_name, "Config"))
    os.makedirs(Path(mod_name, "Harmony"))
    os.makedirs(Path(mod_name, "Ignore"))
    os.makedirs(Path(mod_name, "Prefabs"))
    os.makedirs(Path(mod_name, "Resources"))
    os.makedirs(Path(mod_name, "Scripts"))
    os.makedirs(Path(mod_name, "UIAtlases/ItemIconAtlas"))

    # Copying Templates
    shutil.copy(Path(templates_dir, "ModInfo.xml"), Path(mod_name, "ModInfo.xml"))
    shutil.copy(Path(templates_dir, "ModConfig.xml"), Path(mod_name, "ModConfig.xml"))
    shutil.copy(Path(templates_dir, ".csproj"), Path(mod_name, csproj))
    shutil.copy(Path(templates_dir, "gitignore.template"), Path(mod_name, ".gitignore"))
    shutil.copy(Path(templates_dir, "ModApi.cs"), Path(mod_name, "Harmony/ModApi.cs"))
    shutil.copy(Path(templates_dir, "sdutils.json"), Path(mod_name, "sdutils.json"))

    # Template Rendering
    _render_template(Path(mod_name, csproj), PLACEHOLDERS)
    _render_template(Path(mod_name, "ModInfo.xml"), PLACEHOLDERS)
    _render_template(Path(mod_name, "Harmony/ModApi.cs"), PLACEHOLDERS)
    _render_template(Path(mod_name, "sdutils.json"), PLACEHOLDERS)

    # Git Initialization
    try:
        subprocess.run(f"git init {Path(mod_name)}", capture_output=True)
    except FileNotFoundError:
        print("WRN: error while initializing git repository")