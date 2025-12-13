# 7D2D Utils

## Overview

**7D2D Utils** is a Python-based command-line interface designed to simplify and automate common workflows involved in *7 Days to Die* modding.

It targets mod developers who want a reproducible, scriptable, and efficient workflow without relying on ad-hoc scripts or manual steps.

Key features:

* Automated mod build processes (with or without C# DLLs)
* Fast creation and configuration of new modding projects
* One-command launch of local game sessions or local dedicated servers

## Table of Contents

* [Command Line Features](#command-line-features)
* [Supported Platform](#supported-platform)
* [Installation](#installation)

  * [GitHub installation](#github-installation)
  * [Manual installation (development only)](#manual-installation-development-only)
* [Global Configuration](#global-configuration)
* [Mod Project Configuration](#mod-project-configuration)

  * [Configuration Schema](#configuration-schema)
  * [Example](#example)
* [Configuration Reference](#configuration-reference)
* [License](#license)

## Command Line Features

| Command         | Description                                                                                           |
| --------------- | ----------------------------------------------------------------------------------------------------- |
| `build`         | Compile the project in the current working directory and create a zip archive ready for testing.      |
| `fetch-prefabs` | Copy all prefabs specified in `sdutils.json/prefabs` into the folder `Prefab` of the current project. |
| `infos`         | Show detailed info of the current `sdutils.json` configuration.                                       |
| `install`       | Build the project then install the mod in the 7 Days Mods folder.                                     |
| `new`           | Creates a new 7D2D modding project.                                                                   |
| `release`       | Compile the project and create the release zip archive.                                               |
| `shut-down`     | Hard closes all instances of 7DaysToDie.exe and 7DaysToDieServer.exe.                                 |
| `start`         | Compile the project, then start a local game session.                                                 |

## Supported Platform

* **Operating System**: Windows 10 or later
* **Python**: 3.11 or later
* **.NET Framework**: 4.8 or later (required only for mods containing C# DLLs)

## Installation

### GitHub installation

You can install the latest version of **7D2D Utils** directly from GitHub using pip:

```bash
pip install git+https://github.com/VisualDev-FR/7D2D-Utils.git
```

After installation, the `sdutils` command is available in your terminal.

Verify installation:

```bash
sdutils --help
```

### Manual installation (development only)

Clone the repository:

```bash
git clone https://github.com/VisualDev-FR/7D2D-Utils.git
cd 7D2D-Utils
```

Install in editable mode:

```bash
pip install -e .
```

Intended for contributors or development usage.

## Global Configuration

If you plan to build a C# dll from the provided templates, ensure the environment variable `PATH_7D2D` points to your game directory:

```
setx PATH_7D2D="path/to/steamapps/common/7DaysToDie"
```

On first use, **7D2D Utils** relies on a global configuration file located at:

```
C:/Users/<username>/AppData/Roaming/sdutils.json
```

It defines paths to your *7 Days to Die* installation and user data directories.

### Example

```json
{
    "PATH_7D2D": "path/to/steamapps/common/7 Days To Die",
    "PATH_7D2D_EXE": "path/to/steamapps/common/7 Days To Die/7DaysToDie.exe",
    "PATH_7D2D_SERVER": "path/to/7 Days to Die Dedicated Server/7DaysToDieServer.exe",
    "PATH_7D2D_USER": "path/to/AppData/Roaming/7DaysToDie"
}
```

### Configuration Override

A `sdutils.json` file at the root of a modding project **overrides global configuration**, allowing multiple game versions or environments.


## Mod Project Configuration

Each modding project must define its own `sdutils.json` at the project root, controlling how the mod is built, packaged, and deployed.

## Configuration Schema

| Key            | Type             | Required | Description                                                       |
| -------------- | ---------------- | -------- | ----------------------------------------------------------------- |
| `name`         | `string`         | yes      | Mod identifier used for metadata, defaults, and build outputs.    |
| `csproj`       | `string \| null` | no       | C# project file to build, or `null` if none.                      |
| `include`      | `string[]`       | yes      | Files/directories included in the release archive.                |
| `prefabs`      | `string[]`       | no       | Prefab sources imported from the user data directory.             |
| `dependencies` | `string[]`       | no       | Additional mod dependencies (relative or absolute paths).         |
| `clear_saves`  | `object[]`       | no       | Save directories to clear before running (`world` + `save`).      |
| `game_path`    | `string \| null` | no       | Overrides global *7 Days to Die* game path for this project only. |
| `dedi_path`    | `string \| null` | no       | Overrides global dedicated server path for this project only.     |

### Example

```json
{
    "name": "my-mod-name",
    "csproj": "myProject.csproj",
    "include": [
        "ModInfo.xml",
        "ModConfig.xml",
        "Config",
        "UIAtlases",
        "Resources",
        "Prefabs"
    ],
    "prefabs": [
        "relative/path/to/prefab-to-include"
    ],
    "dependencies": [
        "relative-path/to/another-mod-dir"
    ],
    "clear_saves": [
        {
            "world": "world-name",
            "save": "save-directory-name"
        }
    ],
    "game_path": null,
    "dedi_path": null
}
```

## Configuration Reference

### `name`

Project identifier for:

* Populating `ModInfo.xml`
* Generating code snippets
* Determining default archive name

### `csproj` *(optional)*

C# project to build; `null` if no DLL.

### `include`

Files/directories copied into the release archive.

### `prefabs`

Prefab sources imported from the game user directory.

### `dependencies`

Additional mod dependencies; supports relative and absolute paths.

### `clear_saves`

Saves to clear automatically, when starting the game with `start` command:

```json
"clear_saves": [
    {
        "world": "world-name",
        "save": "save-directory-name"
    }
]
```

### `game_path` / `dedi_path`

Optional overrides for global game or dedicated server paths.

## License

This project is distributed under the MIT License.
