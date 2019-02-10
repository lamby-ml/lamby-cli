import click
import os
import json
import sys


@click.command('init', short_help="initialize .lamby file in cwd")
def init():
    """Initializes the .lamby file in the repository"""

    lamby_dir = './.lamby'
    if os.path.isdir(lamby_dir):
        click.echo('Lamby project already initialized in ' + os.getcwd())
        sys.exit(1)

    os.mkdir(lamby_dir)
    os.mkdir(lamby_dir + '/commit_objects')

    config_file = open(lamby_dir + '/config', "w+")
    config_file.write(json.dumps({}))
    config_file.close()

    log_file = open(lamby_dir + '/log', "w+")
    log_file.write(json.dumps({}))
    log_file.close()

    click.echo('Initializing Lamby project in ' + os.getcwd())
