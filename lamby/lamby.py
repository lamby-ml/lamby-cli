import click
import os
import shutil
import json


@click.group()
def cli():
    pass


@cli.command()
def help():
    # this is modeled after the git help command `git help`

    try:
        click.echo("usage: lamby [--help] <command> [<args>]")
        click.echo("")  # newline
        click.echo("Here are the Lamby commands used in different situations:")
        click.echo("")  # newline
        click.echo("Create a new Lamby project:")
        click.echo("    init — Create an empty Lamby repository"
                   + " in the current directory")
        click.echo("    uninit — Remove all files/data associated"
                   + " with the Lamby repository in the current directory")
    except Exception:
        click.echo("Error. Please try again.")
        return 0

    return 1


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
    click.echo('Commiting following files:')
    for file in files:
        click.echo('\t' + file)
    if message is not None:
        click.echo('Commit Message: ' + message)


if __name__ == '__main__':
    cli()
