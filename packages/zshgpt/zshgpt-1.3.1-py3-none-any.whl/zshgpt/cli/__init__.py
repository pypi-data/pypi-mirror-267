# SPDX-FileCopyrightText: 2023-present Anders Steen <asteennilsen@gmail.com
#
# SPDX-License-Identifier: MIT
import click
from openai import AuthenticationError

from zshgpt.__about__ import __version__
from zshgpt.util.assistant import send_message


@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name='zshgpt')
@click.argument('user_query')
def zshgpt(user_query: str) -> str:
    try:
        response: str = send_message(user_query)
    except AuthenticationError as auth_error:
        raise click.ClickException(auth_error.message) from auth_error
    click.echo(response)
