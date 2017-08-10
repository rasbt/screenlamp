# Sebastian Raschka 2017
#
# screenlamp is a Python toolkit
# for hypothesis-driven virtual screening.
#
# Copyright (C) 2017 Michigan State University
# License: MIT
#
# Software author: Sebastian Raschka <http://sebastianraschka.com>
# Software author email: mail@sebastianraschka.com
#
# Software source repository: https://github.com/rasbt/screenlamp
# Documentation: https://psa-lab.github.io/screenlamp
#
# screenlamp was developed in the
# Protein Structural Analysis & Design Laboratory
# (http://www.kuhnlab.bmb.msu.edu)
#
# If you are using screenlamp in your research, please cite
# the following journal article:
#
# Sebastian Raschka, Anne M. Scott, Nan Liu,
#   Santosh Gunturu, Mar Huertas, Weiming Li,
#   and Leslie A. Kuhn.
# "Screenlamp: A hypothesis-driven, ligand-based toolkit to
#    facilitate large-scale screening,
#    applied to discover potent GPCR inhibitors"


import subprocess
import argparse
import sys
import os
import gzip


def mol_count_python(input_file, zipped):

    if zipped:
        open_cmd = gzip.open
        look_up = b'@<TRIPOS>ATOM'
    else:
        open_cmd = open
        look_up = '@<TRIPOS>ATOM'
    cnt = 0
    with open_cmd(input_file, 'r') as f:
        for line in f:
            if line.startswith(look_up):
                cnt += 1
    return cnt


def mol_count_shell(input_file, zipped):

    if zipped:
        grep = 'zgrep'
    else:
        grep = 'grep'

    ps = subprocess.Popen([grep, "@<TRIPOS>ATOM", input_file],
                          stdout=subprocess.PIPE)
    raw = subprocess.check_output(['wc', '-l'], stdin=ps.stdout)
    ps.wait()

    return int(raw.decode().rstrip())


def count_in_dir(path, windows):

    total = 0
    for f in os.listdir(path):
        if f.endswith(('.mol2', 'mol2.gz')):
            file_path = os.path.join(path, f)
            zipped = f.endswith('.mol2.gz')

            if windows:
                cnt = mol_count_python(file_path, zipped)
            else:
                cnt = mol_count_shell(file_path, zipped)

            sys.stdout.write('%s : %d\n' % (f, cnt))
            sys.stdout.flush()
            total += cnt
    return total


def main(input_name):
    is_dir = os.path.isdir(input_name)
    is_windows = os.system == 'Windows'

    if not is_dir:
        zipped = input_name.endswith('.gz')
        if is_windows:
            total = mol_count_python(input_name, zipped)
        else:
            total = mol_count_shell(input_name, zipped)

    else:
        total = count_in_dir(input_name, is_windows)

    sys.stdout.write('Total : %d\n' % total)
    sys.stdout.flush()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description=('A command line tool for counting the number'
                         ' of molecules in MOL2 files.'),
            epilog="""Example: 
    python count_mol2.py -i mol2_dir/
    python count_mol2.py -i partition_1.mol2""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        required=True,
                        type=str,
                        help='(Required.) Path to a `.mol2` or `.mol2.gz`file,'
                             '\nor a directory containing `.mol2`/`.mol2.gz`'
                             ' files.')

    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    if not args.input:
        parser.print_help()

    else:
        main(args.input)
