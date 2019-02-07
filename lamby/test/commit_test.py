import os
from test.utils import create_file, unzip_to, cmp_files
from src.init import init
from src.commit import commit
from src.utils import deserialize_log


def test_commit_basic(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)

        filename = 'file1.onnx'
        message = 'Foo Bar!'

        create_file(filename, 100)

        result = runner.invoke(commit, [filename, '-m', message])

        assert result.exit_code == 0

        log_file = deserialize_log()
        compressed_filename = './.lamby/commit_objects/' + \
            log_file[filename][0]['hash']
        uncompressed_filename = log_file[filename][0]['hash']

        assert log_file[filename][0]['message'] == message
        assert os.path.isfile(compressed_filename)

        unzip_to(compressed_filename, uncompressed_filename)

        assert cmp_files(filename, uncompressed_filename)


def test_commit_no_spec_file(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)

        os.mkdir('dir1')
        create_file('file1.onnx', 100)
        create_file('dir1/file2.onnx', 100)

        result = runner.invoke(commit, ['-m', 'Foo Bar!'])

        assert result.exit_code == 0

        log_file = deserialize_log()

        compressed_filename = './.lamby/commit_objects/' + \
            log_file['file1.onnx'][0]['hash']
        uncompressed_filename = log_file['file1.onnx'][0]['hash']

        assert os.path.isfile(compressed_filename)

        unzip_to(compressed_filename, uncompressed_filename)

        assert cmp_files('file1.onnx', uncompressed_filename)

        compressed_filename = './.lamby/commit_objects/' + \
            log_file['file2.onnx'][0]['hash']
        uncompressed_filename = log_file['file2.onnx'][0]['hash']

        assert os.path.isfile(compressed_filename)

        unzip_to(compressed_filename, uncompressed_filename)

        assert cmp_files('dir1/file2.onnx', uncompressed_filename)
