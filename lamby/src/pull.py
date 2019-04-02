import os
import sys

import click

from lamby.src.utils import (deserialize_config, deserialize_log,
                             deserialize_meta, get_request, serialize_log,
                             serialize_meta, unzip_to)


@click.command('pull', short_help='pull changes from lamby web')
def pull():
    '''Pulls all new commits from remote Lamby repository'''

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    config = deserialize_config()
    if 'project_id' not in config:
        click.echo('No Lamby project detected.')
        sys.exit(1)
    project_id = deserialize_config()['project_id']

    res = get_request('/api/projects/{}'.format(project_id))

    res_json = res.json()

    log = deserialize_log()

    commits_in_log = set()
    for k in log:
        for c in log[k]:
            commits_in_log.add(c['hash'])

    commits_to_download = []
    for commit_hash in res_json['commits']:
        if commit_hash not in commits_in_log:
            commits_to_download.append(commit_hash)

    from lamby.filestore import fs
    for c_hash in commits_to_download:
        fs.download_file_from_key(
            str(project_id) + '/' + c_hash, lamby_dir + '/commit_objects/'
            + c_hash)

        c_filename = res_json['commits'][c_hash]['filename']
        if c_filename not in log:
            log[c_filename] = []

        log[c_filename].append({
            'timestamp': int(res_json['commits'][c_hash]['timestamp']),
            'message': res_json['commits'][c_hash]['message'],
            'hash': c_hash
        })

    meta = deserialize_meta()
    for c_hash in res_json['heads']:
        c_filename = res_json['heads'][c_hash]['filename']
        if c_filename not in meta['file_head']:
            meta['file_head'][c_filename] = {'index': 0}

        meta['file_head'][c_filename]['hash'] = c_hash
        unzip_to('./.lamby/commit_objects/'+c_hash, './'+c_filename)

    for c_hash in res_json['latest_commits']:
        c_filename = res_json['latest_commits'][c_hash]['filename']
        meta['latest_commit'][res_json['latest_commits']
                              [c_hash]['filename']] = c_hash

    serialize_log(log)
    serialize_meta(meta)

    sys.exit(0)
