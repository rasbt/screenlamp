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
import os
import sys
import time

from biopandas.mol2.mol2_io import split_multimol2


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


def mol2_to_idfile(mol2_files, id_file_path, verbose=0):
    with open(id_file_path, 'w') as f:
        for mol2_file in mol2_files:

            if verbose:
                sys.stdout.write('Processing %s' % os.path.basename(mol2_file))
                sys.stdout.flush()
                start = time.time()

            for idx, mol2 in enumerate(split_multimol2(mol2_file)):
                f.write(mol2[0] + '\n')

            if verbose:
                elapsed = time.time() - start
                n_molecules = idx + 1
                sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                                 (n_molecules, n_molecules / elapsed))
                sys.stdout.flush()


def main(input_dir, output_file, verbose):
    mol2_files = get_mol2_files(dir_path=input_dir)
    mol2_to_idfile(mol2_files=mol2_files,
                   id_file_path=output_file,
                   verbose=verbose)
    if verbose:
        print('Finished')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Writes a file with molecule IDs from MOL2 files.',
            epilog="""Example:
python mol2_to_id.py\\
   --input mol2_dir\\
   --output ids.txt""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='(Required.) Input `.mol2` or `.mol2.gz` file,'
                             'or a directory of MOL2 files.')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Output path for the ID file.'
                             ' For example, `ids.txt`.')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='(Optional, default: `1`.)'
                             ' Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(args.input, args.output, args.verbose)
