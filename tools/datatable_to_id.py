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

            if selection is not None:
                mask = pd.eval(selection)
            else:
                mask = chunk.index
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

    columns = [id_column]
    if selection is None:
        parsed_sele = None
    else:
        parsed_sele = parse_selection_string(selection, df_name='chunk')
        columns += columns_from_selection(selection)

    dirpath = os.path.dirname(output_file)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

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
            epilog='Example:\n'
                   'python datatable_to_id.py -i table.txt -o ids.txt \\'
                   '\n --id_column ZINC_ID --selection "(NRB <= 7) & (MWT > 200)"\n',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Path to a datatable file where each row'
                             '\nrepresents a molecule and each columns'
                             '\nstore the molecular features')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output path for the ID file.'
                             ' For example, ids.txt')
    parser.add_argument('--id_column',
                        type=str,
                        required=True,
                        help='Name of the Molecule ID column')
    parser.add_argument('--seperator',
                        type=str,
                        default='\t',
                        help='Column seperator used\nin the input table')
    parser.add_argument('-s', '--selection',
                        type=str,
                        default=None,
                        help='Selection condition.\n'
                        'single column selection example: (MWT > 500)\n'
                        'logical OR example: (MWT > 500) | (MWT < 200)\n'
                        'logical AND example: (NRB <= 7) & (MWT > 200)')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             '\noutput.'
                             '\nIf 1 (default), prints the file currently'
                             '\nprocessing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(args.input, args.output, args.verbose, args.selection, args.id_column)
