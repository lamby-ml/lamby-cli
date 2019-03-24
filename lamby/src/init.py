import json
import os
import sys

import click


@click.command('init', short_help="initialize .lamby file in cwd")
def init():
    """Initializes the .lamby file in the repository"""

    lamby_dir = os.path.join(os.path.realpath('.'), '.lamby')

    if os.path.isdir(lamby_dir):
        click.echo('Lamby project already initialized in ' + os.getcwd())
        sys.exit(1)

    os.mkdir(lamby_dir)
    os.mkdir(os.path.join(lamby_dir, 'commit_objects'))

    with open(lamby_dir + '/config', "w+") as config_file:
        config_file.write(json.dumps({}))

    with open(lamby_dir + '/log', "w+") as log_file:
        log_file.write(json.dumps({}))

    with open(lamby_dir + '/meta', "w+") as meta_file:
        meta_file.write(json.dumps({
            'file_head': {},
            'latest_commit': {}
        }))

    click.echo('Initialized Lamby project in ' + os.getcwd())
