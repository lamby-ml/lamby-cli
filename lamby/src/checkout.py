import sys

import click

from lamby.src.utils import (deserialize_log, deserialize_meta, diff_files,
                             fetch_commit, search_pattern, serialize_meta,
                             copy_file)


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
        sys.exit(1)
    elif len(results) > 1:
        for result in results:
            click.echo('{} [{}]'.format(result[0], result[2]))
        sys.exit(0)

    result = results[0]
    result_name = result[0]
    result_index = result[1]
    result_hash = result[2]

    if result_name in meta['file_head'] \
            and meta['file_head'][result_name]['hash'] == result_hash:
        click.echo('Hash is currently head')
    else:
        fetch_commit(result_hash)
        fetch_commit(meta['file_head'][result_name]['hash'])

        file_search_results = search_pattern('./**/' + result_name)
        # TODO: add check for duplicate filenames
        file_path = file_search_results[0]

        if not diff_files(file_path, './.lamby/commit_objects/' +
                          meta['file_head'][result_name]['hash']):
            click.echo('Cannot checkout with uncommitted changes')
            sys.exit(1)

        copy_file('./.lamby/commit_objects/' + result_hash, file_path)

        meta['file_head'][result_name] = {
            'hash': result_hash,
            'index': result_index
        }

        serialize_meta(meta)
