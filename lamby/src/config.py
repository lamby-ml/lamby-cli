import click
import sys
import os
from src.utils import serialize_config, deserialize_config


@click.command('config', short_help='modify configuration parameters')
@click.option('--add', nargs=2, help='usage: --add [key] [value] — adds' +
              ' key/value pair to config file')
@click.option('--change', nargs=2, help='usage: --change [key] [value] ' +
              '— changes key to have given value in config file')
@click.option('--remove', nargs=1, help='usage: --remove [key] ' +
              '— removes the selected key from the config file')
def config(add, change, remove):
    """Modify configuration parameters for this initialized Lamby project"""

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):  # Check if current dir has .lamby file
        click.echo('Lamby project not initialized in ' + os.getcwd())
        sys.exit(1)

    data = deserialize_config()

    # add #

    if len(add) != 0:
        if add[0] in data:
            click.echo("This key already exists")
        else:
            data[add[0]] = add[1]
    if len(change) != 0:
        if change[0] not in data:
            click.echo("This key does not exist")
        else:
            data[change[0]] = change[1]
    if remove is not None:
        del data[remove]

    serialize_config(data)
