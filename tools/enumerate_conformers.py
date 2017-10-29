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

import os
import argparse
import sys
import time
import gzip
from biopandas.mol2 import split_multimol2


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


def read_and_write(inp_mol2_path, out_mol2_path, verbose):

    if verbose:
        sys.stdout.write('Processing %s' % os.path.basename(inp_mol2_path))
        sys.stdout.flush()
        start = time.time()


    if inp_mol2_path.endswith('.gz'):
        write_mode = 'wb'
        open_file = gzip.open
    else:
        write_mode = 'w'
        open_file = open

    """
    if query_path.endswith('.gz'):
        for id_, cont in split_multimol2(query_path):
            cnt += 1
            cont = b''.join(cont).decode('utf-8').split('\n')
            if multiconf_query:
                mol_idx = '%s_%d' % (id_.decode('utf-8'), cnt)
            else:
                mol_idx = id_
    """

    with open_file(out_mol2_path, write_mode) as outfile:

        prev_molecule = ''

        if inp_mol2_path.endswith('.gz'):
            for i, (id_, cont) in enumerate(split_multimol2(inp_mol2_path)):
                if prev_molecule != id_:
                    cnt = 0
                else:
                    cnt += 1

                mol_idx = b'%s_%d' % (id_, cnt)

                cont[1] = mol_idx + b'\n'
                outfile.write(b''.join(cont))
                prev_molecule = id_

        else:
            for i, (id_, cont) in enumerate(split_multimol2(inp_mol2_path)):
                if prev_molecule != id_:
                    cnt = 0
                else:
                    cnt += 1

                mol_idx = '%s_%d' % (id_, cnt)

                cont[1] = mol_idx + '\n'
                outfile.write(''.join(cont))
                prev_molecule = id_

    if verbose:
        elapsed = time.time() - start
        n_molecules = i + 1
        sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                         (n_molecules, n_molecules / elapsed))
        sys.stdout.flush()


def main(input_dir, output_dir, verbose):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    inp_mol2_paths = get_mol2_files(input_dir)

    for mol2_path in inp_mol2_paths:
        base = os.path.basename(mol2_path)
        out_mol2_path = os.path.join(output_dir, base)
        read_and_write(mol2_path, out_mol2_path, verbose)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Numbers molecules in MOL2 files by'
                        ' adding a suffix as index.'
                        ' For example, if there are three'
                        ' molecules in a MOL2 file,'
                        ' moleculeabc_0, moleculeabc_1, and moleculedef_0,'
                        '\n those molecules will be relabeled to'
                        ' moleculeabc_0, moleculeabc_1, and moleculedef_0.',
            epilog="""Example:
python enumerate_conformers.py -i conformer_mol2s/\\
   --output numbered_conformers/""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        required=True,
                        type=str,
                        help='(Required.) Path to a `.mol2` or `.mol2.gz`file,'
                             '\nor a directory containing `.mol2`/`.mol2.gz`'
                             ' files.')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Directory path for writing the'
                             ' numbered MOL2s')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             '\nIf 1 (default), prints the file currently'
                             '\nprocessing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(input_dir=args.input,
         output_dir=args.output,
         verbose=args.verbose)
