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
import gzip

from biopandas.mol2.mol2_io import split_multimol2


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


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


def read_idfile(id_file_path):
    with open(id_file_path, 'r') as f:
        ids = {line.strip() for line in f if not line.startswith('#')}
    return ids


def filter_and_write(mol2_files, ids, output_dir, includelist_filter, verbose):
    for mol2_file in mol2_files:
        if verbose:
            sys.stdout.write('Processing %s' % os.path.basename(mol2_file))
            sys.stdout.flush()

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        mol2_outpath = os.path.join(output_dir, os.path.basename(mol2_file))

        if mol2_outpath.endswith('.gz'):
            write_mode = 'wb'
            open_file = gzip.open
        else:
            write_mode = 'w'
            open_file = open

        with open_file(mol2_outpath, write_mode) as f:
            if verbose:
                start = time.time()

            if includelist_filter:

                if write_mode == 'w':
                    for idx, mol2 in enumerate(split_multimol2(mol2_file)):

                        if mol2[0] in ids:
                            f.write(''.join(mol2[1]))
                else:
                    for idx, mol2 in enumerate(split_multimol2(mol2_file)):

                        if mol2[0].decode('utf-8') in ids:
                            f.write(b''.join(mol2[1]))

            else:
                if write_mode == 'w':
                    for idx, mol2 in enumerate(split_multimol2(mol2_file)):
                        if mol2[0] not in ids:
                            f.write(''.join(mol2[1]))
                else:
                    for idx, mol2 in enumerate(split_multimol2(mol2_file)):
                        if mol2[0].decode('utf-8') not in ids:
                            f.write(b''.join(mol2[1]))
            if verbose:
                elapsed = time.time() - start
                n_molecules = idx + 1
                sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                                 (n_molecules, n_molecules / elapsed))
                sys.stdout.flush()



def main(input_dir, id_file_path, output_dir, includelist_filter, verbose):
    mol2_files = get_mol2_files(dir_path=input_dir)
    ids = read_idfile(id_file_path)

    filter_and_write(mol2_files=mol2_files,
                     ids=ids,
                     output_dir=output_dir,
                     includelist_filter=includelist_filter,
                     verbose=verbose)
    if verbose:
        print('Finished')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Create filtered MOL2 files from ID and'
                        ' input MOL2 files.',
            epilog="""Example:
python id_to_mol2.py --input mol2_dir/\\
   --id_file ids.txt\\
   --includelist True\\
   --output filtered_mol2_dir/""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='(Required.) Input `.mol2` or `.mol2.gz` file,'
                             ' or a directory of MOL2 files.')
    parser.add_argument('--id_file',
                        type=str,
                        required=True,
                        help='(Required.) Input ID file that contains molecule'
                             '\nIDs (one ID per line).')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Output directory path for the'
                             '\nfiltered MOL2 files.')
    parser.add_argument('-w', '--includelist',
                        type=str2bool,
                        default=True,
                        help='(Optional, default: `True`.) Uses ID file as includelist if True (default).'
                        '\nUses ID file as excludelist if False.')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='(Optional, default: `1`.) Verbosity level. If 0, does not print any'
                             '\noutput.'
                             '\nIf 1 (default), prints the file currently'
                             '\nprocessing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(input_dir=args.input,
         id_file_path=args.id_file,
         output_dir=args.output,
         includelist_filter=args.includelist,
         verbose=args.verbose)
