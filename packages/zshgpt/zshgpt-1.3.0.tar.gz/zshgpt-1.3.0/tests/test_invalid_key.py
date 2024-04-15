from click.testing import CliRunner


def test_invalid_key():
    from src.zshgpt.cli import zshgpt

    runner = CliRunner()
    result = runner.invoke(zshgpt, ['# Can I speak with you?'])
    assert result.exit_code == 1
    assert result.exception
