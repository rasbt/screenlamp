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
from multiprocessing import cpu_count
from numpy import nan as np_nan
from mputil import lazy_imap
from biopandas.mol2 import PandasMol2
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


def get_atom_matches(q_pdmol, d_pdmol):
    atoms, charges = [], []
    for xyz in q_pdmol.df[['x', 'y', 'z']].iterrows():
        distances = d_pdmol.distance(xyz=xyz[1].values)
        nearest_idx = distances.argmin()
        columns = ['atom_type', 'charge']
        if distances.iloc[nearest_idx] > THRESHOLD:
            atom, charge = '', np_nan
        else:
            atom, charge = d_pdmol.df[columns].iloc[nearest_idx].values
        atoms.append(atom)
        charges.append(charge)
    return atoms, charges


def data_processor(mol2s):

    q_pdmol = PandasMol2()
    d_pdmol = PandasMol2()

    d_pdmol.read_mol2_from_list(mol2_code=mol2s[0][0],
                                mol2_lines=mol2s[0][1])

    q_pdmol.read_mol2_from_list(mol2_code=mol2s[1][0],
                                mol2_lines=mol2s[1][1])

    atoms, charges = get_atom_matches(q_pdmol, d_pdmol)
    return mol2s[0][0], mol2s[1][0], atoms, charges


def data_processor_gz(mol2s_gz):

    q_pdmol = PandasMol2()
    d_pdmol = PandasMol2()

    d_pdmol.read_mol2_from_list(mol2_code=mol2s_gz[0][0],
                                mol2_lines=mol2s_gz[0][1])

    q_pdmol.read_mol2_from_list(mol2_code=mol2s_gz[1][0],
                                mol2_lines=mol2s_gz[1][1])

    atoms, charges = get_atom_matches(q_pdmol, d_pdmol)
    return (mol2s_gz[0][0].decode('utf-8'),
            mol2s_gz[1][0].decode('utf-8'),
            atoms, charges)


def read_and_write(q_path, d_path, verbose,
                   cache, output_file, n_cpus):

    dct_results = {'dbase': [], 'query': [], 'atoms': [], 'charges': []}

    d_base = os.path.basename(d_path)
    q_base = os.path.basename(q_path)

    if verbose:
        start = time.time()
        sys.stdout.write('Processing %s/%s' % (d_base, q_base))
        sys.stdout.flush()

    cnt = 0

    if q_path.endswith('.gz'):
        data_processor_fn = data_processor_gz
    else:
        data_processor_fn = data_processor

    for chunk in lazy_imap(data_processor=data_processor_fn,
                           data_generator=zip(split_multimol2(d_path),
                                              split_multimol2(q_path)),
                           n_cpus=n_cpus):

        for dbase_id, query_id, atoms, charges in chunk:
            dct_results['dbase'].append(dbase_id)
            dct_results['query'].append(query_id)
            dct_results['atoms'].append(atoms)
            dct_results['charges'].append(charges)

        cnt += len(chunk)
    """

    q_pdmol = PandasMol2()
    d_pdmol = PandasMol2()

    for q_mol2, d_mol2 in zip(split_multimol2(q_path),
                              split_multimol2(d_path)):
        cnt += 1
        d_pdmol.read_mol2_from_list(mol2_code=d_mol2[0],
                                    mol2_lines=d_mol2[1])
        d_pdmol._df = d_pdmol.df[(d_pdmol.df['atom_type'] != 'H')]

        if q_mol2[0] in cache:
            q_pdmol = cache[q_mol2[0]]

        else:
            q_pdmol.read_mol2_from_list(mol2_code=q_mol2[0],
                                        mol2_lines=q_mol2[1])
            q_pdmol._df = q_pdmol.df[(q_pdmol.df['atom_type'] != 'H')]
            cache[q_mol2[0]] = q_pdmol

        atoms, charges = get_atom_matches(q_pdmol, d_pdmol)

        dct_results['query'].append(q_mol2[0])
        dct_results['dbase'].append(d_mol2[0])
        dct_results['atoms'].append(atoms)
        dct_results['charges'].append(charges)
    """

    with open(output_file + '_charge.tsv', 'w') as f1,\
            open(output_file + '_atomtype.tsv', 'w') as f2:

        columns = PandasMol2().read_mol2(q_path).df['atom_name'].values
        f1.write('dbase\tquery\t%s\n' % '\t'.join(columns))
        f2.write('dbase\tquery\t%s\n' % '\t'.join(columns))
        for i in range(len(dct_results['dbase'])):
            s1 = '%s\t%s\t%s\n' % (dct_results['dbase'][i],
                                 dct_results['query'][i],
                                 '\t'.join(format(x, "1.2f")
                                          for x in dct_results['charges'][i]))

            f1.write(s1)
            s2 = '%s\t%s\t%s\n' % (dct_results['dbase'][i],
                                 dct_results['query'][i],
                                 '\t'.join(dct_results['atoms'][i]))
            f2.write(s2)

    if verbose:
        elapsed = time.time() - start
        n_molecules = cnt + 1
        sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                         (n_molecules, n_molecules / elapsed))
        sys.stdout.flush()


def get_num_cpus(n_cpus):
    if not n_cpus:
        n_cpus = cpu_count()
    elif n_cpus < 0:
        n_cpus = cpu_count() - n_cpus
    return n_cpus


def main(input_dir, output_dir, verbose, n_cpus):

    n_cpus = get_num_cpus(n_cpus)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    mol2_in_files = get_mol2_files(input_dir)

    q_list, d_list = get_dbase_query_pairs(mol2_in_files)

    csv_out_bases = [os.path.join(output_dir,
                                  os.path.basename(mol2).replace(
                                    '_dbase.mol2.gz', '').replace(
                                    '_dbase.mol2', ''))
                     for mol2 in d_list]

    cache = {}
    for q, d, c in zip(q_list, d_list, csv_out_bases):
        read_and_write(q_path=q,
                       d_path=d,
                       verbose=verbose,
                       cache=cache,
                       output_file=c,
                       n_cpus=n_cpus)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Generates tab-separated tables with containing atom'
            '\n type and charge information from matching'
            '\n atoms in pair-wise overlays.\n',
            epilog="""Example:
python funcgroup_matching.py\\
   --input rocs_overlays_sorted/\\
   --output matching_tables/\\
   --max_distance 1.3\\
   --processes 0""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='(Required.) Path to a directory containing pairs '
                             '\nof `*_query.mol2`/`.mol2.gz` '
                             '\nand `*_dbase.mol2`/`.mol2.gz` files')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Path to a directory for writing'
                             '\nthe output files')
    parser.add_argument('-d', '--max_distance',
                        type=float,
                        default=1.3,
                        help='(Optional, default: `1.3`.) The maximum distance,'
                        '\nin angstroms, the'
                        '\noverlayed atoms can be apart from each'
                        '\nother for being considered a match.'
                        '\nFor instance, a --max_distance 1.3 (default)'
                        '\nwould count atoms as a match if they'
                        '\nare within 0 and 1.3 angstroms'
                        '\nto the target atom.')
    parser.add_argument('--processes',
                        type=int,
                        default=1,
                        help='(Optional, default: `1`.) Number of processes to'
                             ' run in parallel.'
                             '\nIf processes > 0, the specified number of CPUs'
                             '\nwill be used.'
                             '\nIf processes = 0, all available CPUs will'
                             '\nbe used.'
                             '\nIf processes = -1, all available CPUs'
                             '\nminus `processes` will be used.')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='(Optional, default: `1`.) Verbosity level. If 0,'
                             ' does not print any output.'
                             '\nIf 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()
    THRESHOLD = args.max_distance

    main(input_dir=args.input,
         output_dir=args.output,
         verbose=args.verbose,
         n_cpus=args.processes)
