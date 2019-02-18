import click
import os
import sys
from src.utils import (
    serialize_log,
    deserialize_log
)


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

    click.echo('Rename successful')
