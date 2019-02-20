from src.status import status
from src.init import init
from src.commit import commit
from src.uninit import uninit
from src.checkout import checkout
from src.utils import (
    deserialize_log
)
from test.utils import (
    create_file
)


def test_status_basic(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)

        create_file('f1.onnx', 100)
        create_file('f2.onnx', 100)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        result = runner.invoke(status)
        assert result.exit_code == 0

        result = runner.invoke(uninit)
        assert result.exit_code == 0


def test_status_update(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)
        create_file('f1.onnx', 100)
        create_file('f2.onnx', 100)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        create_file('f1.onnx', 200)
        result = runner.invoke(status)
        assert result.exit_code == 0


def test_status_previous(runner):
    with runner.isolated_filesystem():

        runner.invoke(init)
        create_file('f1.onnx', 100)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        create_file('f1.onnx', 200)

        result = runner.invoke(commit)
        assert result.exit_code == 0

        log = deserialize_log()

        checkout_hash = log['f1.onnx'][0]['hash']

        result = runner.invoke(checkout, [checkout_hash])
        assert result.exit_code == 0

        result = runner.invoke(status)
        assert result.exit_code == 0
