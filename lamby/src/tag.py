import os
import sys

import click

from lamby.src.utils import deserialize_log, serialize_log


@click.command('tag', short_help='tag a commit')
@click.argument('commits', nargs=-1)
@click.option('-t', '--tag', help='usage: -t/--tag [tag]' +
              ' — tags all commits with specified tag')
def tag(commits, tag):
    """Tags a specific commit with given tag in the version history."""

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):
        click.echo('Lamby project has not been initialized in ' + os.getcwd())
        sys.exit(1)

    if tag is None:
        # Not listing and didn't provide a tag
        click.echo('Please include a tag using -t <tag>')
        sys.exit(1)

    if len(commits) == 0:
        click.echo('Please indicate commit ID of commit to tag.')
        sys.exit(1)
    else:
        click.echo('Tagging following commit(s):')
        log = deserialize_log()
        for filename in log.keys():
            log_commits = log[filename]
            for commit_dict in log_commits:
                if commit_dict["hash"] in commits:
                    click.echo("\t" + commit_dict["hash"][0:6] +
                               ": " + commit_dict["message"])
                    commit_dict["tag"] = tag

    click.echo('Tag: ' + tag)
    serialize_log(log)
    sys.exit(0)
