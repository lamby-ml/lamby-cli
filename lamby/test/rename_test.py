import os
from src.rename import rename
from src.utils import deserialize_log


def test_rename_basic(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = '{\"test.onnx\": \"TESTDATA\"}'

        file.write(log_str)
        file.close()

        result = runner.invoke(rename, ['test.onnx', 'renamed.onnx'])

        assert result.exit_code == 0

        log = deserialize_log()

        assert 'test.onnx' not in log
        assert 'renamed.onnx' in log
        assert log['renamed.onnx'] == 'TESTDATA'


def test_rename_bad_file_name(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = '{\"test.onnx\": \"TESTDATA\"}'

        file.write(log_str)
        file.close()

        result = runner.invoke(rename, ['bad.onnx', 'wooo.onnx'])

        assert result.exit_code == 1


def test_rename_bad_file_rename(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        log_str = '{\"test.onnx\": \"TESTDATA\"}'

        file.write(log_str)
        file.close()

        result = runner.invoke(rename, ['bad.onnx', 'wooo.onnx'])

        assert result.exit_code == 1


def test_rename_uninit_lamby(runner):
    with runner.isolated_filesystem():

        result = runner.invoke(rename, ['test.onnx', 'test.onnx'])

        assert result.exit_code == 1
