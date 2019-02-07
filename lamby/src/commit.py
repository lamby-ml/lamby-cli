import click
import os
import time
import hashlib
import gzip
import sys
import glob
from lamby.lamby import cli
from src.utils import (
    serialize_log,
    deserialize_log,
    diff_gzip,
    file_sha256
)


@cli.command('commit', short_help='commit changes that have been made')
@click.argument('files', nargs=-1)
@click.option('-m', '--message')
def commit(files, message):
    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    files = search_file_type('.', 'onnx') if len(files) == 0 else files
    if len(files) == 0:
        click.echo('There are no onnx files in the project directory.')
        sys.exit(1)

    log = deserialize_log()

    file_errors = False

    for file in files:
        basename = os.path.basename(file)

        if not os.path.isfile(file):
            click.echo(file + ' is not a file')
            file_errors = True

        if file.split('.')[-1] != 'onnx':
            click.echo(file + ' is not an onnx file')
            file_errors = True

        if basename in log and diff_gzip(file, './.lamby/commit_objects/' +
                                         log[basename][-1]['hash']):
            click.echo(file + ' has no changes to commit')
            file_errors = True

    if file_errors:
        sys.exit(1)

    for file in files:

        basename = os.path.basename(file)

        if basename not in log:
            log[basename] = []

        commit_record = {}
        commit_record["timestamp"] = int(time.time())
        commit_record["message"] = str(message)

        str_to_hash = basename
        str_to_hash += str(commit_record["timestamp"])
        str_to_hash += commit_record["message"]
        str_to_hash += file_sha256(file)

        if len(log[basename]) > 0:
            str_to_hash += log[basename][-1]["hash"]

        str_to_hash = str_to_hash.encode("utf-8")

        hash_gen = hashlib.sha256(str_to_hash).hexdigest()

        commit_record["hash"] = hash_gen

        log[basename].append(commit_record)

        with open(file, 'rb') as commit_file:
            with gzip.open('./.lamby/commit_objects/'
                           + hash_gen, 'wb') as zipped_commit:
                zipped_commit.writelines(commit_file)
                zipped_commit.close()
                commit_file.close()

    serialize_log(log)

    click.echo('Committed the following files:')
    for file in files:
        click.echo('\t' + os.path.basename(file))
    click.echo("Commit message: \"" + message + "\"")


def search_file_type(directory, ftype):
    results = []
    for file in glob.iglob(directory + '/**/*.' + ftype, recursive=True):
        results.append(file)
    return results
