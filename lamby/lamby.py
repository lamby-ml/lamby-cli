import click
from lib.init import init
from lib.commit import commit
from lib.uninit import uninit


@click.group()
def cli():
    pass


cli.add_command(init)
cli.add_command(commit)
cli.add_command(uninit)

if __name__ == '__main__':
    cli()
