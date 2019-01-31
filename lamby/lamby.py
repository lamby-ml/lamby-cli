import click
import os
import shutil
import json


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
    click.echo('Commiting following files:')
    for file in files:
        click.echo('\t' + file)
    if message is not None:
        click.echo('Commit Message: ' + message)


if __name__ == '__main__':
    cli()
