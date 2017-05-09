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


import argparse
import sys
import pandas as pd


def read_and_write(source, target, selection, id_column, sep, verbose):

    parsed_sele = parse_selection_string(selection, df_name='chunk')
    columns = [id_column] + columns_from_selection(selection)

    if verbose:
        counter = 0
        print('Using columns: %s' % columns)
        print('Using selection: %s' % parsed_sele)

    reader = pd.read_table(source, chunksize=100000, usecols=columns, sep=sep)

    with open(target, 'w') as f:
        for chunk in reader:
            mask = pd.eval(parsed_sele)
            chunk.loc[mask, [id_column]].to_csv(f,
                                                header=None,
                                                index=None)
            if verbose:
                counter += 100000
                sys.stderr.write('\rProcessed: %d' % counter)
                sys.stderr.flush()

    if verbose:
        n_lines = sum(1 for line in open(target, 'r'))
        sys.stdout.write('\nSelected: %d\n' % n_lines)
        sys.stdout.flush()


def parse_selection_string(s, df_name='chunk'):
    return s.replace('(', '(%s.' % df_name)


def columns_from_selection(s):
    return [c.replace('(', '') for c in s.split() if '(' in c]


def main(input_dir, output_file, verbose):
    read_and_write(source=args.input,
                   target=args.output,
                   selection=args.selection,
                   id_column=args.id_column,
                   sep=args.seperator,
                   verbose=args.verbose)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Write a file with molecule IDs from MOL2 files.',
            epilog='Example: python mol2_to_id.py -i mol2_dir -o ids.txt\n',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input .mol2 or .mol2.gz file,'
                             'or a directory of MOL2 files')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output path for the ID file.'
                             ' For example, ids.txt')
    parser.add_argument('--id_column',
                        type=str,
                        required=True,
                        help='ID column.')
    parser.add_argument('--seperator',
                        type=str,
                        default='\t',
                        help='Column seperator')
    parser.add_argument('-s', '--selection',
                        type=str,
                        required=True,
                        help='Selection string For example, ...')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(args.input, args.output, args.verbose)
