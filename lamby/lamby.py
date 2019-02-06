import click
# from init import init
from commit import commit
# from uninit import uninit


@click.group()
def cli():
    pass


# cli.add_command(init)
cli.add_command(commit)
# cli.add_command(uninit)

if __name__ == '__main__':
    cli()
