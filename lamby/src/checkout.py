import click
from src.utils import (
    serialize_meta,
    deserialize_meta,
    deserialize_log,
    search_pattern,
    unzip_to
)


@click.command('checkout', short_help='checkout a commit hash')
@click.argument('hash', nargs=1)
def checkout(hash):
    '''Checks out the binary files associated with a commit hash'''

    meta = deserialize_meta()
    log = deserialize_log()

    results = []

    for file_name in log.keys():
        for ci, commit in enumerate(log[file_name]):
            if commit['hash'].startswith(hash):
                results.append((file_name, ci, commit['hash']))

    if len(results) == 0:
        click.echo('Commit hash not found')
        return
    elif len(results) > 1:
        for result in results:
            click.echo('{} [{}]'.format(result[0], result[2]))
        return

    result = results[0]
    result_name = result[0]
    result_index = result[1]
    result_hash = result[2]
    if result_name in meta['file_head'] \
            and meta['file_head'][result_name]['hash'] == result_hash:
        click.echo('Hash is currently head')
    else:
        file_search_results = search_pattern('./**/' + result_name)
        # TODO: add check for duplicate filenames
        file_path = file_search_results[0]

        unzip_to('./.lamby/commit_objects/' + result_hash, file_path)

        meta['file_head'][result_name] = {
            'hash': result_hash,
            'index': result_index
        }

        serialize_meta(meta)
