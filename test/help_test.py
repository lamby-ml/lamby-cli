from click.testing import CliRunner
from lamby.lamby import help


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(help, [])

        assert result.exit_code == 0
