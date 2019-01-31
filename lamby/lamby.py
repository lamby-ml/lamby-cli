import click
import os
import shutil
import json
import time
import hashlib


@click.group()
def cli():
    pass


@cli.command()
def init():
    lamby_dir = os.getcwd() + '/.lamby'
    if os.path.isdir(lamby_dir):
        click.echo('Lamby project already initialized in ' + os.getcwd())
        return

    os.mkdir(lamby_dir)

    config_file = open(lamby_dir + '/config', "w+")
    config_file.write(json.dumps({}))
    config_file.close()

    log_file = open(lamby_dir + '/log', "w+")
    log_file.write(json.dumps({}))
    log_file.close()

    click.echo('Initializing Lamby project in ' + os.getcwd())


@cli.command()
def uninit():
    lamby_dir = os.getcwd() + '/.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        return
    click.echo('Removing Lamby project in ' + os.getcwd())

    shutil.rmtree(lamby_dir)


@cli.command()
@click.argument('files', nargs=-1)
@click.option('-m', '--message')
def commit(files, message):
    lamby_dir = os.getcwd() + '/.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        return

    log = deserialize_log()

    for file in files:
        if file not in log:
            log[file] = []

        commit_record = {}
        commit_record["timestamp"] = int(time.time())
        commit_record["message"] = message

        str_to_hash = os.path.basename(file)
        str_to_hash += str(commit_record["timestamp"])
        str_to_hash += commit_record["message"]
        str_to_hash += file_sha256(file)

        if len(log[file]) > 0:
            str_to_hash += log[file][-1]["hash"]

        str_to_hash = str_to_hash.encode("utf-8")

        commit_record["hash"] = hashlib.sha256(str_to_hash).hexdigest()
        log[file].append(commit_record)

    serialize_log(log)


def deserialize_log():
    if not os.path.isfile(os.getcwd() + '/.lamby/log'):
        return {}
    with open(os.getcwd() + '/.lamby/log') as log_file:
        return json.load(log_file)


def deserialize_config():
    if not os.path.isfile(os.getcwd() + '/.lamby/config'):
        return {}
    with open(os.getcwd() + '/.lamby/config') as config_file:
        return json.load(config_file)


def serialize_log(data):
    with open(os.getcwd() + '/.lamby/log', 'w+') as log_file:
        log_file.write(json.dumps(data))
        log_file.close()


def serialize_config(data):
    with open(os.getcwd() + '/.lamby/config', 'w+') as config_file:
        config_file.write(json.dumps(data))
        config_file.close()


def file_sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


if __name__ == '__main__':
    cli()
