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
# Documenatation: https://psa-lab.github.io/screenlamp
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


import argparse
import sys
import os
import pandas as pd
import time


def read_and_write(source, target, selection,
                   columns, id_column, sep, verbose):

    if verbose:
        counter = 0
        sys.stdout.write('Using columns: %s\n' % columns)
        sys.stdout.write('Using selection: %s\n' % selection)
        sys.stdout.flush()

    reader = pd.read_table(source, chunksize=100000, usecols=columns, sep=sep)

    with open(target, 'w') as f:
        if verbose:
            start = time.time()
        for chunk in reader:

            mask = pd.eval(selection)
            chunk.loc[mask, [id_column]].to_csv(f,
                                                header=None,
                                                index=None)
            if verbose:
                counter += chunk.shape[0]

                elapsed = time.time() - start
                sys.stdout.write('\rProcessed %d rows | %d rows/sec' %
                                 (counter, counter / elapsed))
                sys.stderr.flush()

    if verbose:
        n_lines = sum(1 for line in open(target, 'r'))
        sys.stdout.write('\nSelected: %d\n' % n_lines)
        sys.stdout.flush()


def parse_selection_string(s, df_name='chunk'):
    return s.replace('(', '(%s.' % df_name)


def columns_from_selection(s):
    return [c.replace('(', '') for c in s.split() if '(' in c]


def main(input_dir, output_file, verbose, selection, id_column):

    parsed_sele = parse_selection_string(selection, df_name='chunk')
    dirpath = os.path.dirname(output_file)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    columns = [id_column] + columns_from_selection(selection)
    read_and_write(source=args.input,
                   target=args.output,
                   selection=parsed_sele,
                   columns=columns,
                   id_column=id_column,
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

    main(args.input, args.output, args.verbose, args.selection, args.id_column)
