import os
from src.init import init
from src.uninit import uninit


def test_uninit(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(init, [])
        result = runner.invoke(uninit, [])

        assert result.exit_code == 0
        assert not os.path.isdir('./.lamby')
