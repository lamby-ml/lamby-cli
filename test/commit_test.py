import os
import gzip
import shutil
import filecmp
from test.utils import create_file
from lamby.lamby import init, commit, deserialize_log


def test_commit_basic(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)

        filename = "file1.txt"
        message = "Foo Bar!"

        create_file(filename, 100)

        result = runner.invoke(commit, [filename, "-m", message])

        assert result.exit_code == 0

        log_file = deserialize_log()
        compressed_filename = './.lamby/commit_objects/' + \
            log_file[filename][0]["hash"]
        uncompressed_filename = log_file[filename][0]["hash"]

        assert log_file[filename][0]["message"] == message
        assert os.path.isfile(compressed_filename)

        with gzip.open(compressed_filename, 'rb') as compressed_file:
            with open(uncompressed_filename, 'wb') as uncompressed_file:
                shutil.copyfileobj(compressed_file, uncompressed_file)
                compressed_file.close()
                uncompressed_file.close()

        filecmp.clear_cache()
        assert filecmp.cmp(filename, uncompressed_filename)
