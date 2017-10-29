# Sebastian Raschka 2017
#
# screenlamp is a Python toolkit
# for hypothesis-driven virtual screening.
#
# Copyright (C) 2017 Michigan State University
# License: Apache v2
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
# Raschka, Sebastian,  Anne M. Scott, Nan Liu,
#   Santosh Gunturu, Mar Huertas, Weiming Li,
#   and Leslie A. Kuhn. 2017
#
# Enabling the hypothesis-driven prioritization of
#   ligand candidates in big databases:
#   Screenlamp and its application to GPCR inhibitor
#   discovery for invasive species control.
#


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
                   sep=args.separator,
                   verbose=args.verbose)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Create a text file with molecule IDs from MOL2 files.',
            epilog="""Example:
python datatable_to_id.py\\
  --input table.txt\\
  --output ids.txt\\
  --id_column ZINC_ID\\
  --selection "(NRB <= 7) & (MWT > 200)" """,
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='(Required.) Path to a datatable file where each'
                             '\nrow represents a molecule and each columns'
                             '\nstore the molecular features.')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Output path for the ID file'
                             ' (for example, `ids.txt`).')
    parser.add_argument('--id_column',
                        type=str,
                        required=True,
                        help='(Required.) Name of the Molecule ID column.')
    parser.add_argument('--separator',
                        type=str,
                        default='\t',
                        help=('(Optional, default: `"\t"`.) Column separator used\nin the input table.\n'
                              'Assumes tab-separated values by default.'))
    parser.add_argument('-s', '--selection',
                        type=str,
                        default=None,
                        help='(Optional, default: `None`.) A conditional selection string:\n'
                        ' Single column selection example: `"(MWT > 500)"`. '
                        ' Logical OR example: `"(MWT > 500) | (MWT < 200)"`.'
                        ' Logical AND example: `"(NRB <= 7) & (MWT > 200)"`.')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='(Optional, default: `1`.) Verbosity level. If 0, does not print any'
                             '\noutput.'
                             '\nIf 1 (default), prints the file currently'
                             '\nprocessing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(args.input, args.output, args.verbose, args.selection, args.id_column)
