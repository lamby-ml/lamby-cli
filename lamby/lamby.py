import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', 'help'])


@click.group()
def cli():
    """
    usage: lamby [--help] <command> [<args>]

    Here are the Lamby commands used in different situations:

    Create a new Lamby project:
        init — Create an empty Lamby repository in the current directory
        uninit — Remove all files/data associated with the Lamby repository
                 in the current directory
    """
    pass


if __name__ == '__main__':
    cli()
