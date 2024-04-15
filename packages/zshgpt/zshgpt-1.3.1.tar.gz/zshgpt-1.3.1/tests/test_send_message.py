import pytest
from click.testing import CliRunner

from zshgpt.cli import zshgpt


@pytest.mark.need_OPENAI_API_KEY
def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(zshgpt, args=['# List my files'])
    assert result.exit_code == 0
    assert result.output
