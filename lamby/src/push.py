import click
import requests
import json
import os
import sys

from src.utils import (deserialize_config, deserialize_meta, deserialize_log)


@click.command('push', short_help='push changes to lamby web')
def push():
    '''Pushes all new commits \
        from local repository to remote Lamby repository'''

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    gc_path = os.path.dirname(os.path.abspath(__file__))+'/.config'
    if not os.path.isfile(gc_path):
        click.echo('No authorization found. Please run lamby auth.')
        sys.exit(1)

    with open(gc_path) as global_config:
        gc_json = json.load(global_config)

    log = deserialize_log()
    payload = {'log': log}
    header = {'x-auth': gc_json['api_key']}

    config = deserialize_config()
    if 'project_id' not in config:
        click.echo('No Lamby project detected.')
        sys.exit(1)
    project_id = deserialize_config()['project_id']

    try:
        res = requests.post(os.getenv('LAMBY_WEB_URI') +
                            '/api/projects/status/{}'.format(project_id),
                            json=payload, headers=header)
    except requests.exceptions.ConnectionError:
        click.echo('Could not reach lamby web. Aborting push.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        click.echo('Connection timed out. Aborting push.')
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        click.echo(
            'Too many redirects to reach lamby web. Aborting push.')
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(e)
        sys.exit(1)

    res_json = res.json()
    commits_to_upload = res_json['commits_to_upload']
    from filestore import fs
    for filename in commits_to_upload:
        for commit in commits_to_upload[filename]:
            fs.upload_file(lamby_dir+'/commit_objects/' +
                           commit['hash'], project_id)

    payload = res_json
    payload['meta'] = deserialize_meta()

    try:
        res = requests.post(os.getenv('LAMBY_WEB_URI') +
                            '/api/projects/push/{}'.format(project_id),
                            json=payload, headers=header)
    except requests.exceptions.ConnectionError:
        click.echo('Could not reach lamby web. Aborting push.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        click.echo('Connection timed out. Aborting push.')
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        click.echo(
            'Too many redirects to reach lamby web. Aborting push.')
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(e)
        sys.exit(1)

    click.echo(res.json()['message'])
    sys.exit(0)
