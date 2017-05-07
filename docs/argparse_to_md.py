# Tool to generate a markdown documentation
# from argparse scripts.
#
# usage: python argparse_to_md.py scipts/ > doc.md
#
# Copyright (C) 2017 Sebastian Raschka
# License: MIT
#
# Author: Sebastian Raschka <http://sebastianraschka.com>
# Author email: mail@sebastianraschka.com


import subprocess
import os
import sys


def get_pyfiles(path):
    files = []
    for file in os.listdir(path):
        if file.endswith('.py'):
            files.append(os.path.join(os.path.abspath(path), file))
    return files


def get_help_messages(path):
    s = subprocess.check_output('python %s --help' % path, shell=True)
    return s.decode()


def help_to_md(s):
    out_lines = []

    for line in s.split('\n'):

        if not line:
            continue

        if line.startswith('usage:'):
            usage = line.split('usage:')[-1].strip()
            out_lines.append('\n**Usage:**\n\n    %s\n\n' % usage)

        elif line.startswith('optional arguments:'):
            out_lines.append('\n**Optional Arguments:**\n\n')

        elif line.startswith('  -'):
            out_lines.append('- `%s`' % line.lstrip())

        elif line.startswith('Example: '):
            usage = line.split('Example:')[-1].strip()
            out_lines.append('\n**Example:**\n\n```\n%s\n```' % usage)

        else:
            if line.startswith('  '):
                line = '    - ' + line.strip()
            out_lines.append(line + '\n')

    return out_lines


def main(dir_path):
    contents = []
    paths = get_pyfiles(dir_path)
    for f in paths:
        contents.append('\n\n# %s\n\n' % os.path.basename(f))
        s = get_help_messages(f)
        lines = help_to_md(s)
        contents.extend(lines)
    for line in contents:
        print(line)


if __name__ == '__main__':
    main(sys.argv[1])
