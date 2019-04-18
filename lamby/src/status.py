import sys

import click

from lamby.src.utils import deserialize_meta, diff_files, search_pattern


@click.command('status', short_help='check the status of the .onnx files in ' +
               'the current project')
def status():
    '''Gives a status update for the .onnx files in the cwd'''

    meta = deserialize_meta()
    files = []
    for file in meta['file_head']:
        files.append(file)

    if len(files) == 0:
        click.echo('There are no onnx files in the project directory.')
        sys.exit(1)

    for file in files:
        file_search_results = search_pattern('./**/' + file)
        # TODO: add check for duplicate filenames
        file_name = file_search_results[0]

        file_head = meta["file_head"][file]["hash"]
        latest_commit = meta["latest_commit"][file]
        if file_head != latest_commit:
            click.echo(
                file+': On a previous hash starting with '+file_head[:4])
            click.echo(file+': Latest hash starts with ' +
                       latest_commit[:4])
        if not diff_files(file_name, './.lamby/commit_objects/' +
                          meta["file_head"][file]["hash"]):
            click.echo(file_name+': This file has uncommitted changes')
