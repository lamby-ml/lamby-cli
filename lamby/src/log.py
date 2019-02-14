import click
import os
import sys
import datetime
from src.utils import (
    deserialize_log
)


@click.command('log', short_help="show commit log")
@click.argument('files', nargs=-1)
@click.option('-a', '--all', is_flag=True, help='usage: -a/--all — ' +
              'show logs for all files in the repository')
@click.option('-c', '--count', help='usage: -c/--count [count] — ' +
              'show [count] last commits', default=5, show_default=True)
def log(files, all, count):
    """Show information about most recent commits of speicified files"""

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    if (not all) and len(files) == 0:
        click.echo('Please include files you want to see the commit logs for' +
                   ' or include -a tag to see commit logs for all files.')
        sys.exit(1)

    log = deserialize_log()
    if all:
        files = log.keys()

    for f in files:
        if f not in log:
            click.echo(f + ' cannot be found in your lamby repository.')
            sys.exit(1)

    for f in files:
        click.echo('\nFile: ' + f + '\n')
        for i in range(max([0-count, 0-len(log[f])]), 0):
            click.echo('\tCommit ID: ' + log[f][i]['hash'])
            date = datetime.datetime.fromtimestamp(
                log[f][i]['timestamp']).strftime('%a %b %-d %-H:%M:%S %Y %z')
            click.echo('\tDate:      ' + date)
            click.echo('\tMessage:   ' + log[f][i]['message'])
            click.echo('\n')

    sys.exit(0)
