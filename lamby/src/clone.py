import os
import shutil

import click

from lamby.src.init import init
from lamby.src.utils import (get_request, serialize_config, serialize_log,
                             serialize_meta, unzip_to)


@click.command('clone', short_help='clone a repository into current directory')
@click.argument('project_id', nargs=1)
def clone(project_id):
    """Clones a repository into the current directory via a URL"""

    from lamby.filestore import fs
    res_nojson = get_request('/api/projects/{}'.format(project_id))

    res = res_nojson.json()

    project_name = res['project_name']
    if os.path.exists(project_name):
        shutil.rmtree(project_name)
    os.mkdir(project_name)
    os.chdir(project_name)

    click.get_current_context().invoke(init)

    lamby_dir = os.path.join(os.path.realpath('.'), '.lamby')
    commit_objects_dir = os.path.join(lamby_dir, 'commit_objects')

    commit_ids = list(res['commits'].keys())
    for commit_id in commit_ids:
        click.echo("Importing: {}".format(commit_id))
        path = f"{commit_objects_dir}/{commit_id}"
        fs.download_file_from_key(
            "{}/{}".format(project_id, commit_id), path
        )

    log = dict()
    for commit_id in commit_ids:

        if res["commits"][commit_id]["filename"] not in log:
            log[res["commits"][commit_id]["filename"]] = []

        commit_record = {}
        commit_record["timestamp"] = res["commits"][commit_id]["timestamp"]
        commit_record["message"] = res["commits"][commit_id]["message"]
        commit_record["hash"] = commit_id

        log[res["commits"][commit_id]["filename"]].append(commit_record)

    serialize_log(log)

    meta = dict()
    meta["file_head"] = dict()
    meta["latest_commit"] = dict()

    head_chunks = list(res["heads"].keys())
    for chunk in head_chunks:
        meta["file_head"][res["commits"][chunk]["filename"]] = {
            'hash': chunk,
            'index': len(log[res["commits"][chunk]["filename"]]) - 1
        }
        filename = res["commits"][chunk]["filename"]
        unzip_to(f"{commit_objects_dir}/{commit_id}", filename)

    latest_chunks = list(res["latest_commits"].keys())
    for chunk in latest_chunks:
        meta["latest_commit"][res["commits"][chunk]["filename"]] = chunk

    serialize_meta(meta)

    config = dict()
    config['project_id'] = project_id

    serialize_config(config)
