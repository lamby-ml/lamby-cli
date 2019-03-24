import shutil
from test.utils import cmp_files, create_file, mutate_file

from src.checkout import checkout
from src.commit import commit
from src.init import init
from src.utils import deserialize_log, deserialize_meta


def test_checkout_basic(runner):
    with runner.isolated_filesystem():

        assert runner.invoke(init).exit_code == 0

        filename = 'file1.onnx'
        create_file(filename, 100)
        shutil.copyfile(filename, './copy')

        assert runner.invoke(commit, [filename]).exit_code == 0

        mutate_file(filename, 100)

        assert runner.invoke(commit, [filename]).exit_code == 0

        log = deserialize_log()

        checkout_hash = log[filename][0]['hash']

        result = runner.invoke(checkout, [checkout_hash])

        meta = deserialize_meta()

        assert result.exit_code == 0
        assert cmp_files('./copy', filename)
        assert meta['file_head'][filename]['hash'] == checkout_hash
        assert meta['file_head'][filename]['index'] == 0


def test_checkout_invalid_commit(runner):
    with runner.isolated_filesystem():
        assert runner.invoke(init).exit_code == 0
        filename = 'file1.onnx'
        create_file(filename, 100)
        assert runner.invoke(commit, [filename]).exit_code == 0
        mutate_file(filename, 100)
        assert runner.invoke(commit, [filename]).exit_code == 0

        result = runner.invoke(checkout, ['foobar'])

        assert result.exit_code == 1
        assert result.output == 'Commit hash not found\n'


def test_checkout_uncommitted_changes(runner):
    with runner.isolated_filesystem():
        assert runner.invoke(init).exit_code == 0
        filename = 'file1.onnx'
        create_file(filename, 100)
        assert runner.invoke(commit, [filename]).exit_code == 0
        mutate_file(filename, 100)
        assert runner.invoke(commit, [filename]).exit_code == 0

        mutate_file(filename, 100)

        log = deserialize_log()

        result = runner.invoke(checkout, [log[filename][0]['hash']])

        assert result.exit_code == 1
        assert result.output == 'Cannot checkout with uncommitted changes\n'
