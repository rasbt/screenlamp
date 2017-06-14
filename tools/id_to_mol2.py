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


def filter_and_write(mol2_files, ids, output_dir, whitelist_filter, verbose):
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

            if whitelist_filter:

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



def main(input_dir, id_file_path, output_dir, whitelist_filter, verbose):
    mol2_files = get_mol2_files(dir_path=input_dir)
    ids = read_idfile(id_file_path)

    filter_and_write(mol2_files=mol2_files,
                     ids=ids,
                     output_dir=output_dir,
                     whitelist_filter=whitelist_filter,
                     verbose=verbose)
    if verbose:
        print('Finished')


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
    parser.add_argument('--id_file',
                        type=str,
                        required=True,
                        help='Input ID file that contains molecule'
                             'IDs (one ID per line)')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output directory path for the'
                             ' filtered MOL2 files')
    parser.add_argument('-w', '--whitelist',
                        type=str2bool,
                        default=True,
                        help='Uses ID file as whitelist if True (default).'
                        ' Uses ID file as blacklist if False.')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(input_dir=args.input,
         id_file_path=args.id_file,
         output_dir=args.output,
         whitelist_filter=args.whitelist,
         verbose=args.verbose)
