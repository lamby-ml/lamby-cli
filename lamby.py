import click
import os
import shutil


@click.group()
def cli():
    pass


@cli.command()
def init():
    if os.path.isdir(os.getcwd() + '/.lamby'):
        click.echo('Lamby project already initialized in ' + os.getcwd())
        return
    click.echo('Initializing Lamby project in ' + os.getcwd())

    os.mkdir(os.getcwd() + '/.lamby')


@cli.command()
def uninit():
    if not os.path.isdir(os.getcwd() + '/.lamby'):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        return
    click.echo('Removing Lamby project in ' + os.getcwd())

    shutil.rmtree(os.getcwd() + '/.lamby')


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
