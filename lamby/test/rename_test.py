import os

from lamby.src.rename import rename
from lamby.src.utils import deserialize_log, deserialize_meta


def test_rename_basic(runner):
    with runner.isolated_filesystem():

        os.mkdir('./.lamby')
        file = open('./.lamby/log', 'w+')
        meta = open('./.lamby/meta', 'w+')
        log_str = '{\"test.onnx\": \"TESTDATA\"}'
        meta_str = """{
                        \"file_head\": {
                        \"test.onnx\": \"TESTDATA\"
                        },
                        \"latest_commit\": {
                        \"test.onnx\": \"TESTDATA\"
                        }
                        }
                   """

        file.write(log_str)
        meta.write(meta_str)
        file.close()
        meta.close()

        result = runner.invoke(rename, ['test.onnx', 'renamed.onnx'])

        assert result.exit_code == 0

        log = deserialize_log()
        meta = deserialize_meta()

        assert 'test.onnx' not in log
        assert 'test.onnx' not in meta['file_head']
        assert 'test.onnx' not in meta['latest_commit']
        assert 'renamed.onnx' in log
        assert 'renamed.onnx' in meta['file_head']
        assert 'renamed.onnx' in meta['latest_commit']
        assert log['renamed.onnx'] == 'TESTDATA'
        assert meta['file_head']['renamed.onnx'] == 'TESTDATA'
        assert meta['latest_commit']['renamed.onnx'] == 'TESTDATA'


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
