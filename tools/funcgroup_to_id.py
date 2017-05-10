# Sebastian Raschka 2017
#
# `screenlamp` is a Python toolkit for using
# filters and pipelines for hypothesis-driven
# virtual screening.
#
# Copyright (C) 2017 Michigan State University
# License: MIT
#
# SiteInterlock was developed in the
# Protein Structural Analysis & Design Laboratory
# (http://www.kuhnlab.bmb.msu.edu)
#
# Author: Sebastian Raschka <http://sebastianraschka.com>
# Author email: mail@sebastianraschka.com


import os
import argparse
import pandas as pd
from biopandas.mol2 import split_multimol2
from biopandas.mol2 import PandasMol2


def get_mol2_files(dir_path):

    files = []

    if os.path.isdir(dir_path):
        for f in os.listdir(dir_path):
            if f.endswith(('.mol2', 'mol2.gz')):
                file_path = os.path.join(dir_path, f)
                files.append(file_path)

    elif (os.path.isfile(dir_path) and
          dir_path.endswith(('.mol2', 'mol2.gz'))):
        files.append(dir_path)

    return files


def parse_selection_string(s, df_name='pdmol.df'):
    columns = ['(atom_id', '(atom_name', '(atom_type',
               '(subst_id', '(subst_name', '(charge']
    for c in columns:
        s = s.replace(c, '(%s.%s' % (df_name, c[1:]))
    return s


def read_and_write(mol2_files, id_file_path, selection, verbose):

    total_count = 0
    with open(id_file_path, 'w') as f:

        for mol2_file in mol2_files:
            count = 0
            if verbose:
                print('Processing %s' % mol2_file)

            pdmol = PandasMol2()
            for mol2 in split_multimol2(mol2_file):
                pdmol.read_mol2_from_list(mol2_lines=mol2[1],
                                          mol2_code=mol2[0])
                print(selection)
                import sys
                sys.exit()
                if pd.eval(selection).any():
                    f.write(mol2[0])
                    count += 1
            if verbose:
                print('  Selected: %d' % count)
                total_count += count
    if verbose:
        print('Total Selected: %d' % total_count)


def main(input_dir, output_file, selection, verbose):
    mol2_files = get_mol2_files(dir_path=input_dir)
    parsed_sele = parse_selection_string(selection)
    read_and_write(mol2_files=mol2_files,
                   id_file_path=output_file,
                   selection=parsed_sele,
                   verbose=verbose)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='A command line tool for filtering mol2 files.',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        help='Input directory with .mol2 and .mol2.gz files')
    parser.add_argument('-o', '--output',
                        type=str,
                        help='Directory for writing the output files')
    parser.add_argument('-s', '--selection',
                        type=str,
                        required=True,
                        help='Selection string For example, ...')
    parser.add_argument('-p', '--processes',
                        type=int,
                        default=1,
                        help='Number of processes to run in parallel.'
                             ' Uses all CPUs if 0')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(args.input, args.output, args.selection, args.verbose)
