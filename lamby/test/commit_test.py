import os

from lamby.src.commit import commit
from lamby.src.init import init  # NOQA
from lamby.src.utils import deserialize_log, copy_file
from lamby.test.utils import cmp_files, create_file


def test_commit_basic(runner):
    with runner.isolated_filesystem():

        lamby_dir = './.lamby'
        os.mkdir(lamby_dir)
        os.mkdir(lamby_dir + '/commit_objects')

        config_file = open(lamby_dir + '/config', "w+")
        config_file.write('{}')
        config_file.close()

        log_file = open(lamby_dir + '/log', "w+")
        log_file.write('{}')
        log_file.close()

        meta_file = open(lamby_dir + '/meta', "w+")
        meta_file.write('''{
            \"file_head\": {},
            \"latest_commit\": {}
        }''')
        meta_file.close()

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

        copy_file(compressed_filename, uncompressed_filename)

        assert cmp_files(filename, uncompressed_filename)


def test_commit_no_spec_file(runner):
    with runner.isolated_filesystem():

        lamby_dir = './.lamby'
        os.mkdir(lamby_dir)
        os.mkdir(lamby_dir + '/commit_objects')

        config_file = open(lamby_dir + '/config', "w+")
        config_file.write('{}')
        config_file.close()

        log_file = open(lamby_dir + '/log', "w+")
        log_file.write('{}')
        log_file.close()

        meta_file = open(lamby_dir + '/meta', "w+")
        meta_file.write('''{
            \"file_head\": {},
            \"latest_commit\": {}
        }''')
        meta_file.close()

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

        copy_file(compressed_filename, uncompressed_filename)

        assert cmp_files('file1.onnx', uncompressed_filename)

        compressed_filename = './.lamby/commit_objects/' + \
            log_file['file2.onnx'][0]['hash']
        uncompressed_filename = log_file['file2.onnx'][0]['hash']

        assert os.path.isfile(compressed_filename)

        copy_file(compressed_filename, uncompressed_filename)

        assert cmp_files('dir1/file2.onnx', uncompressed_filename)
