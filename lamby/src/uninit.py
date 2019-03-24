import os
import shutil
import sys

import click


@click.command('uninit', short_help="un-initialize .lamby file in cwd")
def uninit():
    """Un-initializes the .lamby file in the repository"""

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)
    click.echo('Removing Lamby project in ' + os.getcwd())

    shutil.rmtree(lamby_dir)
