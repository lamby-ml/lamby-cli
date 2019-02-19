import click
import sys
from src.utils import (
    deserialize_meta,
    search_file_type,
    diff_gzip
)


@click.command('status', short_help='check the status of the .onnx files in ' +
               'the current project')
def status():
    '''Gives a status update for the .onnx files in the cwd'''

    files = search_file_type('.', 'onnx')

    if len(files) == 0:
        click.echo('There are no onnx files in the project directory.')
        sys.exit(1)

    meta = deserialize_meta()

    for file in files:
        file_name = file.split("/")[-1]
        # print(file_name)
        file_head = meta["file_head"][file_name]["hash"]
        latest_commit = meta["latest_commit"][file_name]
        if file_head != latest_commit:
            click.echo(
                file_name+': On a previous hash starting with '+file_head[:4])
            click.echo(file_name+': Latest hash starts with ' +
                       latest_commit[:4])

        if not diff_gzip(file, './.lamby/commit_objects/' +
                         meta['latest_commit'][file_name]):
            click.echo(file_name+': This file has uncommitted changes')
