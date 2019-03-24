import pytest
from click.testing import CliRunner

from filestore import Filestore


@pytest.fixture(scope='package')
def runner():
    return CliRunner()


@pytest.fixture(scope='package')
def test_fs():
    fs = Filestore('testing')
    yield fs
    fs.clear_testing_bucket()
