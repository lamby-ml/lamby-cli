import os

from src.log import log


def test_commit_basic(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = """
        {
            "test.onnx": [
                {
                    "timestamp": 1550182122,
                    "message": "message",
                    "hash": "hash"
                }
            ]
        }
        """
        file.write(log_str)
        file.close()

        result = runner.invoke(log, ['test.onnx'])

        assert result.exit_code == 0
        correct_output = """
File: test.onnx\n
\tCommit ID: hash\n\tDate:      Thu Feb 14 17:08:42 2019 \n\
\tMessage:   message\n\n"""
        assert result.output == correct_output


def test_log_invalid_input(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = """
        {
            "test.onnx": [
                {
                    "timestamp": 1550182122,
                    "message": "message",
                    "hash": "hash"
                }
            ]
        }
        """
        file.write(log_str)
        file.close()

        result = runner.invoke(log, ['wrong_file.onnx'])

        assert result.exit_code == 1
