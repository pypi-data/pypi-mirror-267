import pytest

from zshgpt.util import assistant


@pytest.mark.need_OPENAI_API_KEY
def test_create_assistant():
    a = assistant.create_assistant()
    assert a


@pytest.mark.need_OPENAI_API_KEY
def test_get_assistant():
    a = assistant.get_or_create_assistant()
    assert a
