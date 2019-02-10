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

        with open('./.lamby/config', 'r') as config_file:
            data = config_file.read()
            assert data == ''

        with open('./.lamby/log', 'r') as log_file:
            data = log_file.read()
            assert data == '{}'
