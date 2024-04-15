from time import sleep

from openai.types.beta.assistant import Assistant

from zshgpt.settings import Settings, settings
from zshgpt.util.client import client
from zshgpt.util.messages import messages

INSTRUCTIONS = """You are a zsh terminal assistant. Everything you return will be returned directly in a terminal.
If the user wants a textual answer, remember to put '#' in front of all lines that should not run.
If the user is looking for a terminal command, return the command without #
You are allowed to explain what the command does as long as you put '#' in front of the explenation lines
"""


def get_or_create_assistant() -> str:
    if settings.assistant_id:
        return settings.assistant_id
    existing_assistants = client.beta.assistants.list().data
    existing_zshgpt_assistants = list(filter(lambda a: a.name == settings.assistant_name, existing_assistants))
    if existing_zshgpt_assistants:
        assistant = existing_zshgpt_assistants[0]
        assistant_id = assistant.id
        settings.assistant_id = assistant_id
        Settings.model_validate(settings)
        return assistant.id
    new_assistant = create_assistant()
    assistant_id = new_assistant.id
    settings.assistant_id = assistant_id
    Settings.model_validate(settings)
    return new_assistant.id


def create_assistant() -> Assistant:
    return client.beta.assistants.create(
        name=settings.assistant_name,
        instructions=INSTRUCTIONS,
        model=settings.model,
        tools=[{'type': 'code_interpreter'}],
    )


def get_assistant(assistant_id: str) -> Assistant:
    return client.beta.assistants.retrieve(assistant_id)


def get_or_create_thread() -> str:
    saved_thread_id = settings.thread_id
    if saved_thread_id:
        return saved_thread_id

    new_thread = client.beta.threads.create(messages=messages)
    settings.thread_id = new_thread.id
    return new_thread.id


def get_or_create_a_run() -> str:
    saved_run_id = settings.run_id
    if saved_run_id:
        return saved_run_id

    new_run = client.beta.runs.create(assistant=settings.assistant_id, thread=settings.thread_id)
    settings.run_id = new_run.id
    return new_run.id


def send_message(message: str) -> str:
    """Main public assistant function.

    This function will first get the assistant, a thread, and then send a message to the thread.
    Returns the answer as a string.
    """
    assistant_id = get_or_create_assistant()
    thread_id = get_or_create_thread()
    client.beta.threads.messages.create(thread_id=thread_id, role='user', content=message)
    run = client.beta.threads.runs.create(assistant_id=assistant_id, thread_id=thread_id)
    while run.status in ('queued', 'in_progress'):
        sleep(0.1)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value
