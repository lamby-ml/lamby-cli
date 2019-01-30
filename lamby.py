import click


@click.group()
def cli():
    pass


@cli.command()
def init():
    click.echo('Initializing Lamby.')


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
