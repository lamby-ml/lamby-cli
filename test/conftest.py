import pytest
from click.testing import CliRunner


@pytest.fixture(scope="package")
def runner():
    return CliRunner()
