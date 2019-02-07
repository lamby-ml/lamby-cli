import click
from src.init import init
from src.commit import commit
from src.uninit import uninit


@click.group()
def cli():
    pass


cli.add_command(init)
cli.add_command(commit)
cli.add_command(uninit)

if __name__ == '__main__':
    cli()
