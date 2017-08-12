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
        if file.endswith('.py') and not file.startswith('_'):
            files.append(os.path.join(os.path.abspath(path), file))
    return files


def get_help_messages(path):
    s = subprocess.check_output('python %s --help' % path, shell=True)
    return s.decode()


def help_to_md(s):
    out_lines = []


    example_section = False
    for line in s.split('\n'):

        lstripped = line.lstrip()
        stripped = lstripped.rstrip()

        if not stripped:
            continue

        if stripped == "-v, --version         show program's version number and exit":
            out_lines.append('- `-v, --version`  ')
            out_lines.append("Show program's version number and exit")

        elif stripped == "-h, --help            show this help message and exit":
            out_lines.append('- `-h, --help`  ')
            out_lines.append("Show this help message and exit")

        elif stripped.startswith('Example:'):
            example_section = True
            out_lines.append('\n**Example:**\n\n```')

        elif example_section:
            if stripped.startswith('#'):
                out_lines.append('```\n')
                example_section = False
            out_lines.append(stripped)

        elif stripped.startswith('[-'):
            out_lines.append('`%s`  ' % stripped)

        elif stripped.startswith('usage:'):
            usage = stripped.split('usage:')[-1]
            out_lines.append('\n**Usage:**\n\n    %s\n\n' % usage)

        elif stripped.startswith('optional arguments:'):
            out_lines.append('\n**Arguments:**\n\n')

        elif stripped.startswith('  --') or stripped.startswith('python'):
            out_lines.append('`%s`  ' % stripped)

        elif line.startswith('  -'):
            out_lines.append('- `%s`  ' % stripped)

            #usage = line.split('Example')[-1].strip().strip(':')
            
        else:
            if stripped.startswith('  '):
                stripped = '     ' + stripped.strip()
            out_lines.append(stripped)

    if example_section:
        out_lines.append('```\n')

    return out_lines


def main(dir_path):
    s = ("This page serves as a quick lookup reference for the different"
         " modules within screenlamp. Please see the [Toolkit Tutorial](tools-tutorial-1)"
         " for a"
         " more detailed explanation of the different modules and how"
         " they can be combined in a typical virtual screening pipeline.")

    contents = ["# Tools", "\n", s]
    paths = get_pyfiles(dir_path)
    for f in paths:
        contents.append('\n\n## %s\n\n' % os.path.basename(f))
        s = get_help_messages(f)
        lines = help_to_md(s)
        contents.extend(lines)
    for line in contents:
        print(line)


if __name__ == '__main__':
    main(sys.argv[1])
