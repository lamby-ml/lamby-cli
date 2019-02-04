import click
import os
import shutil
import json
import time
import hashlib
import gzip
import glob
import sys


@click.group()
def cli():
    pass


@cli.command()
def init():
    lamby_dir = './.lamby'
    if os.path.isdir(lamby_dir):
        click.echo('Lamby project already initialized in ' + os.getcwd())
        sys.exit(1)

    os.mkdir(lamby_dir)
    os.mkdir(lamby_dir + '/commit_objects')

    config_file = open(lamby_dir + '/config', "w+")
    config_file.write(json.dumps({}))
    config_file.close()

    log_file = open(lamby_dir + '/log', "w+")
    log_file.write(json.dumps({}))
    log_file.close()

    click.echo('Initializing Lamby project in ' + os.getcwd())


@cli.command()
def uninit():
    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)
    click.echo('Removing Lamby project in ' + os.getcwd())

    shutil.rmtree(lamby_dir)


@cli.command()
@click.argument('files', nargs=-1)
@click.option('-m', '--message')
def commit(files, message):
    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    if len(files) == 0:
        files = search_file_type('.', 'onnx')

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


def deserialize_log():
    if not os.path.isfile('./.lamby/log'):
        return {}
    with open('./.lamby/log') as log_file:
        return json.load(log_file)


def deserialize_config():
    if not os.path.isfile('./.lamby/config'):
        return {}
    with open('./.lamby/config') as config_file:
        return json.load(config_file)


def serialize_log(data):
    with open('./.lamby/log', 'w+') as log_file:
        log_file.write(json.dumps(data))
        log_file.close()


def serialize_config(data):
    with open('./.lamby/config', 'w+') as config_file:
        config_file.write(json.dumps(data))
        config_file.close()


def file_sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
        f.close()
    return hash_sha256.hexdigest()


# Currently done by hash comparison, a little hacky.
def diff_gzip(fname, compressed_object_path):
    current_hash = file_sha256(fname)
    with gzip.open(compressed_object_path, 'rb') as compressed_object:
        compressed_sha = hashlib.sha256()
        for chunk in iter(lambda: compressed_object.read(4096), b""):
            compressed_sha.update(chunk)
        compressed_object.close()
        return current_hash == compressed_sha.hexdigest()


def search_file_type(directory, ftype):
    results = []
    for file in glob.iglob(directory + '/**/*.' + ftype, recursive=True):
        results.append(file)
    return results


if __name__ == '__main__':
    cli()
