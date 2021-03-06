import os

from lamby.src.checkout import checkout
from lamby.src.commit import commit
from lamby.src.init import init
from lamby.src.status import status
from lamby.src.uninit import uninit  # NOQA
from lamby.src.utils import deserialize_log, copy_file
from lamby.test.utils import create_file


def test_status_basic(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        os.mkdir('./.lamby/commit_objects')
        meta_str = """
            {
                "file_head": {
                    "f1.onnx": {
                        "hash": "hash1",
                        "index": 0
                    },
                    "f2.onnx": {
                        "hash": "hash2",
                        "index": 0
                    },
                    "f3.onnx": {
                        "hash": "hash3",
                        "index": 0
                    }
                },
                "latest_commit": {
                    "f1.onnx": "hash1",
                    "f2.onnx": "hash2",
                    "f3.onnx": "hash3"
                }
            }
        """
        file = open('./.lamby/meta', 'w+')
        file.write(meta_str)
        file.close()

        create_file('f1.onnx', 500)
        create_file('f2.onnx', 500)
        create_file('f3.onnx', 500)

        copy_file('f1.onnx', './.lamby/commit_objects/' + "hash1")
        copy_file('f2.onnx', './.lamby/commit_objects/' + "hash2")
        copy_file('f3.onnx', './.lamby/commit_objects/' + "hash3")

        result = runner.invoke(status)
        assert result.exit_code == 0


def test_status_update(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)
        create_file('f1.onnx', 100)
        create_file('f2.onnx', 100)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        create_file('f1.onnx', 200)
        result = runner.invoke(status)
        assert result.exit_code == 0


def test_status_previous(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)
        create_file('f1.onnx', 100)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        create_file('f1.onnx', 200)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        log = deserialize_log()

        checkout_hash = log['f1.onnx'][0]['hash']

        result = runner.invoke(checkout, [checkout_hash])
        assert result.exit_code == 0

        result = runner.invoke(status)
        assert result.exit_code == 0
