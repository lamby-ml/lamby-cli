import os

from src.init import init


def test_init(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(init, [])

        assert result.exit_code == 0
        assert os.path.isdir('./.lamby')
        assert os.path.isdir('./.lamby/commit_objects')
        assert os.path.isfile('./.lamby/config')
        assert os.path.isfile('./.lamby/log')
        assert os.path.isfile('./.lamby/meta')

        with open('./.lamby/config', 'r') as config_file:
            data = config_file.read()
            assert data == '{}'

        with open('./.lamby/log', 'r') as log_file:
            data = log_file.read()
            assert data == '{}'

        with open('./.lamby/meta', 'r') as log_file:
            data = log_file.read()
            assert data == '{"file_head": {}, "latest_commit": {}}'


def test_double_init(runner):
    with runner.isolated_filesystem():

        assert runner.invoke(init).exit_code == 0

        result = runner.invoke(init)

        message = 'Lamby project already initialized in ' + os.getcwd() + '\n'

        assert result.exit_code == 1
        assert result.output == message
