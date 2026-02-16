import click

from .commands.new import cmd_new
from .commands.build import (
    cmd_infos,
    cmd_build,
    cmd_release,
    cmd_install,
    cmd_shut_down,
    cmd_start_local,
    cmd_fetch_prefabs,
)

# Application branding logo in ASCII art
ascii_logo = r"""
  ______ _____      _    _ _______ _____ _       _____
 |____  |  __ \    | |  | |__   __|_   _| |     / ____|
     / /| |  | |___| |  | |  | |    | | | |    | (___
    / / | |  | |___| |  | |  | |    | | | |     \___ \
   / /  | |__| |   | |__| |  | |   _| |_| |____ ____) |
  /_/   |_____/     \____/   |_|  |_____|______|_____/
"""


class CustomHelp(click.Group):
    """
    Overwrites the default Click Help formatter to inject the ASCII art logo
    at the top of the help message.
    """
    def get_help(self, ctx):
        return f"{ascii_logo}\n{super().get_help(ctx)}"


@click.group(cls=CustomHelp, context_settings={"max_content_width": 120})
def cli():
    """
    7D2D Utils: A set of automated commands to manage 7 Days to Die modding projects.

    This CLI handles everything from project scaffolding to building,
    deploying, and launching the game.
    """
    pass


# --- Command Registration ---

# From new.py: Handles project creation
cli.add_command(cmd_new)

# From build.py: Handles build, packaging, and lifecycle management
cli.add_command(cmd_build)
cli.add_command(cmd_release)
cli.add_command(cmd_fetch_prefabs)
cli.add_command(cmd_start_local)
cli.add_command(cmd_shut_down)
cli.add_command(cmd_install)
cli.add_command(cmd_infos)


if __name__ == "__main__":
    cli()