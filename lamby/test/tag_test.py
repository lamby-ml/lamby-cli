import os

from lamby.src.tag import tag
from lamby.src.utils import deserialize_log


def test_tag_basic(runner):
    with runner.isolated_filesystem():
        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = """
        {
            "test.onnx": [
                {
                    "timestamp": 1550098166,
                    "message": "Test Commit",
                    "hash": "testhash"
                }
            ]
        }
        """
        file.write(log_str)
        file.close()

        result = runner.invoke(tag, ["testhash", "-t", "TestTag"])

        assert result.exit_code == 0

        log = deserialize_log()

        assert log["test.onnx"][0]["tag"] == "TestTag"


def test_tag_invalid_input(runner):
    with runner.isolated_filesystem():
        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = """
        {
            "test.onnx": [
                {
                    "timestamp": 1550098166,
                    "message": "Test Commit",
                    "hash": "testhash"
                }
            ]
        }
        """
        file.write(log_str)
        file.close()

        result = runner.invoke(tag, ['incorrect_input'])

        assert result.exit_code == 1
