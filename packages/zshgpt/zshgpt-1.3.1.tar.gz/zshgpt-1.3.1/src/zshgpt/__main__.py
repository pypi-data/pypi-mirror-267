# SPDX-FileCopyrightText: 2023-present Anders Steen <asteennilsen@gmail.com
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == '__main__':
    from zshgpt.cli import zshgpt

    user_arg = sys.argv[1]
    sys.exit(zshgpt(user_arg))
