from src.init import init
from src.config import config


def test_init(runner):
    with runner.isolated_filesystem():

        lamby_dir = './.lamby'

        runner.invoke(init)

        key = "key"
        value = "value"
        change_value = "changed value"
        compare_line = "{\"key\": \"value\"}"
        change_line = "{\"key\": \"changed value\"}"

        # test add #

        result = runner.invoke(config, ['--add', key, value])

        assert result.exit_code == 0

        with open(lamby_dir + '/config', "r") as file:
            for line in file:
                assert(line == compare_line)

        # test change #

        result = runner.invoke(config, ['--change', key, change_value])

        assert result.exit_code == 0

        with open(lamby_dir + '/config', "r") as file:
            for line in file:
                assert(line == change_line)

        # test remove #

        result = runner.invoke(config, ['--remove', key])
        file = open(lamby_dir + '/config', "r")

        assert(file.read() == "{}")
