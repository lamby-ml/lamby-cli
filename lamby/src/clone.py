import click
import os


@click.command('clone', short_help='clone a repository into current directory')
@click.argument('project_id', nargs=1, short_help='ID of project to be cloned')
def clone(project_id):
    """Clones a repository into the current directory via a URL"""
    from filestore import fs

    # need to get the repo name, using repo_url for now
    # the repo_url is the

    dirname = project_id

