import os
import sys

import click

from src.utils import (deserialize_log, deserialize_meta, serialize_log,
                       serialize_meta)


@click.command('rename', short_help='rename file in commit history')
@click.argument('file_original', nargs=1)
@click.argument('file_rename', nargs=1)
def rename(file_original, file_rename):
    """" Renames a file being tracked by the system in all instances """

    if file_rename.split('.')[-1] != 'onnx':
        click.echo(file_rename + ' is not an onnx file')
        sys.exit(1)

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    log = deserialize_log()

    click.echo('Renaming ' + file_original + ' to ' + file_rename)

    if file_original not in log:
        click.echo(file_original + ' cannot be found in your lamby repo')
        sys.exit(1)

    if file_rename in log:
        click.echo(file_rename + ' already exists in your lamby repo')
        sys.exit(1)

    log[file_rename] = log[file_original]
    del log[file_original]
    serialize_log(log)

    meta = deserialize_meta()
    if file_original in meta['file_head']:
        meta['file_head'][file_rename] = meta['file_head'][file_original]
        del meta['file_head'][file_original]
    if file_original in meta['latest_commit']:
        meta['latest_commit'][file_rename] = meta[
            'latest_commit'][file_original]
        del meta['latest_commit'][file_original]
    serialize_meta(meta)

    click.echo('Rename successful')
