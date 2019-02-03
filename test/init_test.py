import os
from lamby.lamby import init, uninit


def test_init(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(init, [])

        assert result.exit_code == 0
        assert os.path.isdir('./.lamby')
        assert os.path.isdir('./.lamby/commit_objects')
        assert os.path.isfile('./.lamby/config')
        assert os.path.isfile('./.lamby/log')

        with open('./.lamby/config', 'r') as config_file:
            data = config_file.read()
            assert data == '{}'

        with open('./.lamby/log', 'r') as log_file:
            data = log_file.read()
            assert data == '{}'


def test_uninit(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(init, [])
        result = runner.invoke(uninit, [])

        assert result.exit_code == 0
        assert not os.path.isdir('./.lamby')
