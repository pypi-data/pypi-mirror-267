import sys

import click
from servicefoundry.cli import create_servicefoundry_cli
from servicefoundry.cli.const import COMMAND_CLS

from truefoundry.autodeploy.exception import GitBinaryNotFoundException

AUTODEPLOY_INSTALLED = True
MLFOUNDRY_INSTALLED = True
GIT_BINARY = True

try:
    from mlfoundry.cli.commands import download
except ImportError:
    MLFOUNDRY_INSTALLED = False

try:
    from truefoundry.autodeploy.cli import autodeploy_cli
except ImportError:
    AUTODEPLOY_INSTALLED = False
except GitBinaryNotFoundException:
    GIT_BINARY = False


@click.group()
def ml():
    """MlFoundry CLI"""


@click.command(name="auto-deploy", cls=COMMAND_CLS)
def handle_git_error():
    """
    Build and deploy projects using Truefoundry
    """
    raise click.UsageError(
        "The 'git' command could not be found. Please ensure Git is available in your system to run auto-deploy."
    )


def main():
    # Exit the interpreter by raising SystemExit(status).
    # If the status is omitted or None, it defaults to zero (i.e., success).
    # If the status is an integer, it will be used as the system exit status.
    # If it is another kind of object, it will be printed and the system exit status will be one (i.e., failure).
    cli = create_servicefoundry_cli()
    if MLFOUNDRY_INSTALLED:
        ml.add_command(download)
        cli.add_command(ml)
    if AUTODEPLOY_INSTALLED:
        if GIT_BINARY:
            cli.add_command(autodeploy_cli)
        else:
            cli.add_command(handle_git_error)

    sys.exit(cli())


if __name__ == "__main__":
    main()
