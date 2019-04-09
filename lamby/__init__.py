import click

from lamby.src.auth import auth
from lamby.src.checkout import checkout
from lamby.src.clone import clone
from lamby.src.commit import commit
from lamby.src.config import config
from lamby.src.init import init
from lamby.src.log import log
from lamby.src.pull import pull
from lamby.src.push import push
from lamby.src.rename import rename
from lamby.src.status import status
from lamby.src.tag import tag
from lamby.src.uninit import uninit
from lamby.src.free import free

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
    from lamby.filestore import fs  # NOQA


cli.add_command(auth)
cli.add_command(init)
cli.add_command(commit)
cli.add_command(checkout)
cli.add_command(uninit)
cli.add_command(tag)
cli.add_command(config)
cli.add_command(rename)
cli.add_command(log)
cli.add_command(status)
cli.add_command(clone)
cli.add_command(pull)
cli.add_command(push)
cli.add_command(free)

if __name__ == '__main__':
    cli()
