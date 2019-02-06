import click
import os
import shutil
import sys


<<<<<<< HEAD:lamby/src/uninit.py
@click.command()
=======
@cli.command('uninit', short_help="un-init the repository"
             + " (delete .lamby folder)")
>>>>>>> fixed flake shit:lamby/uninit.py
def uninit():
    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)
    click.echo('Removing Lamby project in ' + os.getcwd())

    shutil.rmtree(lamby_dir)
