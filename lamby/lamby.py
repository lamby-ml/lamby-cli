import click

from config import init_env
from src.checkout import checkout
from src.commit import commit
from src.config import config
from src.init import init
from src.log import log
from src.rename import rename
from src.status import status
from src.tag import tag
from src.uninit import uninit

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', 'help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    usage: lamby [--help] <command> [<args>]

    Here are the Lamby commands used in different situations:

    Create a new Lamby project:

        init - Create an empty Lamby repository in the current directory
        uninit - Remove all files/data associated with the Lamby repository
                 in the current directory
    """
    init_env()
    from filestore import fs  # NOQA


cli.add_command(init)
cli.add_command(commit)
cli.add_command(checkout)
cli.add_command(uninit)
cli.add_command(tag)
cli.add_command(config)
cli.add_command(rename)
cli.add_command(log)
cli.add_command(status)

if __name__ == '__main__':
    cli()
