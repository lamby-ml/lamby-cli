import click
import sys
from src.utils import (
    serialize_log,
    deserialize_log
)


@click.command('tag', short_help='tag a commit')
@click.argument('commits', nargs=-1)
@click.option('-t', '--tag', help='usage: -t/--tag [tag]' +
              ' — tags all commits with specified tag'
def tag(commits, tag):
    """Tags a specific commit with given tag in the version history."""

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
