import click
from lamby.lamby import cli


@cli.command('help',)
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
