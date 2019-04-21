import os
import sys

import click

from lamby.src.utils import (deserialize_log, deserialize_config, get_request)


@click.command('free', short_help='removes commit objects from local machine')
def free():
    '''Removes all commit objects that are saved locally'''

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    config = deserialize_config()
    if 'project_id' not in config:
        click.echo('No Lamby project detected.')
        sys.exit(1)
    project_id = deserialize_config()['project_id']

    log = deserialize_log()
    commits_in_log = set()
    for k in log:
        for c in log[k]:
            commits_in_log.add(c['hash'])

    res = get_request('/api/projects/{}'.format(project_id))
    res_json = res.json()

    for commit_hash in commits_in_log:
        if commit_hash not in res_json['commits']:
            click.echo('Local repository not in sync with remote repository.')
            click.echo('Please use lamby push before freeing commit objects.')
            sys.exit(1)

    folder = os.path.join(lamby_dir, 'commit_objects')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
