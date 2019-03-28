import click
import os


@click.command('clone', short_help='clone a repository into current directory')
@click.argument('repo_url', nargs=1)
def clone(repo_url):
    """Clones a repository into the current directory via a URL"""
    from filestore import fs

    # need to get the repo name, using repo_url for now
    # the repo_url is the

    dirname = "temp_dir"


