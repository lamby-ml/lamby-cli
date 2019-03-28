import click
import os
import requests
import shutil
import sys
import json
from src.init import init
from src.utils import (
    serialize_log,
    serialize_meta,
    serialize_config
)


@click.command('clone', short_help='clone a repository into current directory')
@click.argument('project_id', nargs=1)
def clone(project_id):
    """Clones a repository into the current directory via a URL"""

    sample_response = """
        {
        "commits": {
            "1be03de7f8015b1cc147474f4ef324ea856c2f38b4d166733307d7af655ba76a": {
            "author": "test9@test.com",
            "filename": "model1.onnx",
            "message": "Test Commit 2",
            "timestamp": 1553738265.1937358
            },
            "27b3ce6beed68344e9302cdf0533a4771e38bca28f371241c88053f1e34cbd2c": {
            "author": "test9@test.com",
            "filename": "model1.onnx",
            "message": "Test Commit 5",
            "timestamp": 1553738265.207747
            },
            "2854e3531d865d258ae913871a2eb4fcb93d291a0dea74e80bce0a7685e07585": {
            "author": "test9@test.com",
            "filename": "model0.onnx",
            "message": "Test Commit 1",
            "timestamp": 1553738265.188274
            },
            "2e7093a0d9181d0b37394327798e5e3eb51da69b74b697e472027286d1b6505c": {
            "author": "test9@test.com",
            "filename": "model0.onnx",
            "message": "Test Commit 4",
            "timestamp": 1553738265.202521
            },
            "80a274cab187934333647e7640c2e477d98e246994a042c0931346ee005a732e": {
            "author": "test9@test.com",
            "filename": "model1.onnx",
            "message": "Test Commit 8",
            "timestamp": 1553738265.22166
            },
            "9824ed34e110a0ff5f9ff4f3957edba82610c45af5d5b9f64763c4130707d7b4": {
            "author": "test9@test.com",
            "filename": "model0.onnx",
            "message": "Test Commit 7",
            "timestamp": 1553738265.216979
            },
            "ac76aae9fc7234b441d006175d9c24100d0e5a769ebd96c4335fe81309636b87": {
            "author": "test9@test.com",
            "filename": "model2.onnx",
            "message": "Test Commit 3",
            "timestamp": 1553738265.1981812
            },
            "b67b1f0049f234031470f0558b8957d94113a593fbba3c7b072176b892bfb004": {
            "author": "test9@test.com",
            "filename": "model2.onnx",
            "message": "Test Commit 9",
            "timestamp": 1553738265.226028
            },
            "c1315939f8727c68bfd23f2060fe094ec6a82fc607efaef96c547492c2361567": {
            "author": "test9@test.com",
            "filename": "model2.onnx",
            "message": "Test Commit 6",
            "timestamp": 1553738265.212321
            }
        },
        "heads": {
            "27b3ce6beed68344e9302cdf0533a4771e38bca28f371241c88053f1e34cbd2c": {
            "author": "test9@test.com",
            "filename": "model1.onnx",
            "message": "Test Commit 5",
            "timestamp": 1553738265.207747
            },
            "2e7093a0d9181d0b37394327798e5e3eb51da69b74b697e472027286d1b6505c": {
            "author": "test9@test.com",
            "filename": "model0.onnx",
            "message": "Test Commit 4",
            "timestamp": 1553738265.202521
            },
            "b67b1f0049f234031470f0558b8957d94113a593fbba3c7b072176b892bfb004": {
            "author": "test9@test.com",
            "filename": "model2.onnx",
            "message": "Test Commit 9",
            "timestamp": 1553738265.226028
            }
        },
        "latest_commits": {
            "80a274cab187934333647e7640c2e477d98e246994a042c0931346ee005a732e": {
            "author": "test9@test.com",
            "filename": "model1.onnx",
            "message": "Test Commit 8",
            "timestamp": 1553738265.22166
            },
            "9824ed34e110a0ff5f9ff4f3957edba82610c45af5d5b9f64763c4130707d7b4": {
            "author": "test9@test.com",
            "filename": "model0.onnx",
            "message": "Test Commit 7",
            "timestamp": 1553738265.216979
            },
            "b67b1f0049f234031470f0558b8957d94113a593fbba3c7b072176b892bfb004": {
            "author": "test9@test.com",
            "filename": "model2.onnx",
            "message": "Test Commit 9",
            "timestamp": 1553738265.226028
            }
        },
        "message": "Succesfully fetched project data",
        "project_name": "testproject"
        }
    """
    res = json.loads(sample_response)
    # print(list(res['commits'].keys()))

    from filestore import fs
    try:
        print("LOL")
        # res_nojson = requests.get(
            # os.getenv('LAMBY_WEB_URI') + '/api/projects/{}'.format(project_id))
    except requests.exceptions.ConnectionError:
        click.echo('Could not reach lamby web. Aborting clone.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        click.echo('Connection timed out. Aborting clone.')
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        click.echo(
            'Too many redirects to reach lamby web. Aborting clone.')
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(e)
        sys.exit(1)

    # res = res_nojson.json()

    project_name = res['project_name']
    if os.path.exists(project_name):
        shutil.rmtree(project_name)
    os.mkdir(project_name)
    os.chdir(project_name)

    click.get_current_context().invoke(init)

    commit_ids = list(res['commits'].keys())
    for commit_id in commit_ids:
        click.echo("Importing: {}".format(commit_id))
        fs.download_file_from_key(
            "{}/{}".format(project_id, commit_id), commit_id)

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

    latest_chunks = list(res["latest_commits"].keys())
    for chunk in latest_chunks:
        meta["latest_commit"][res["commits"][chunk]["filename"]] = chunk

    serialize_meta(meta)

    config = dict()
    config['project_id'] = project_id

    serialize_config(config)
