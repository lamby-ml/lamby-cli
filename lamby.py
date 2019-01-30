import click


@click.group()
def cli():
    pass


@cli.command()
def init():
    click.echo('Initializing Lamby.')


@cli.command()
def commit():
    click.echo('Commiting current files.')


if __name__ == '__main__':
    cli()
