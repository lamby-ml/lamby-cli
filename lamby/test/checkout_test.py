import shutil
from test.utils import create_file, mutate_file, cmp_files
from src.init import init
from src.commit import commit
from src.checkout import checkout
from src.utils import deserialize_log, deserialize_meta


def test_checkout_basic(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)

        filename = 'file1.onnx'
        create_file(filename, 100)
        shutil.copyfile(filename, './copy')

        result = runner.invoke(commit, [filename])

        assert result.exit_code == 0

        mutate_file(filename, 100)

        result = runner.invoke(commit, [filename])

        assert result.exit_code == 0

        log = deserialize_log()

        checkout_hash = log[filename][0]['hash']

        result = runner.invoke(checkout, [checkout_hash])

        meta = deserialize_meta()

        assert result.exit_code == 0
        assert cmp_files('./copy', filename)
        assert meta['file_head'][filename]['hash'] == checkout_hash
        assert meta['file_head'][filename]['index'] == 0
