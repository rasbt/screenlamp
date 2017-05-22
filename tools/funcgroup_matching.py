import os
import argparse
import sys
import time
import pandas as pd
from biopandas.mol2 import PandasMol2
from biopandas.mol2 import split_multimol2

# make mol2.gz compatible


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


def get_dbase_query_pairs(all_mol2s):
    q_list, d_list = [], []
    for m in all_mol2s:
        if m.endswith(('_query.mol2.gz', '_query.mol2')):
            q_list.append(m)
        elif m.endswith(('_dbase.mol2.gz', '_dbase.mol2')):
            d_list.append(m)
    if len(q_list) != len(q_list):
        raise ValueError('The input directory contains an unequal number of'
                         '*_dbase* and *_query* files.')
    return q_list, d_list


def read_and_write(q_path, d_path, verbose, cache):

    d_base = os.path.basename(d_path)
    q_base = os.path.basename(q_path)

    if verbose:
        sys.stdout.write('Processing %s/%s' % (d_base, q_base))
        sys.stdout.flush()

    q_pdmol = PandasMol2()
    d_pdmol = PandasMol2()

    for q_mol2, d_mol2 in zip(split_multimol2(q_path),
                              split_multimol2(d_path)):

        d_pdmol.read_mol2_from_list(mol2_code=d_mol2[0],
                                    mol2_lines=d_mol2[1])
        d_pdmol.df[(d_pdmol.df['atom_type'] != 'H')]

        if q_mol2[0] in cache:
            q_pdmol = cache[q_mol2[0]]

        else:
            q_pdmol.read_mol2_from_list(mol2_code=q_mol2[0],
                                        mol2_lines=q_mol2[1])
            q_pdmol.df[(q_pdmol.df['atom_type'] != 'H')]
            cache[q_mol2[0]] = q_pdmol

    """
    if verbose:
        elapsed = time.time() - start
        n_molecules = cnt + 1
        sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                         (n_molecules, n_molecules / elapsed))
        sys.stdout.flush()
    """






def main(input_dir, output_dir, verbose):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    inp_mol2_paths = get_mol2_files(input_dir)
    q_list, d_list = get_dbase_query_pairs(inp_mol2_paths)


    cache = {}
    for q, d in zip(q_list, d_list):
        read_and_write(q, d, verbose, cache)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='A command line tool for filtering mol2 files.',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory with .mol2 and .mol2.gz files')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Directory for writing the output files')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(input_dir=args.input, output_dir=args.output, verbose=args.verbose)
