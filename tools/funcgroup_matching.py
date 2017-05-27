import os
import argparse
import sys
import time
from numpy import nan as np_nan
from mputil import lazy_imap
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
    d_pdmol._df = d_pdmol.df[(d_pdmol.df['atom_type'] != 'H')]

    q_pdmol.read_mol2_from_list(mol2_code=mol2s[1][0],
                                mol2_lines=mol2s[1][1])
    q_pdmol._df = q_pdmol.df[(q_pdmol.df['atom_type'] != 'H')]

    atoms, charges = get_atom_matches(q_pdmol, d_pdmol)
    return mol2s[0][0], mol2s[1][0], atoms, charges


def read_and_write(q_path, d_path, verbose, cache, output_file):

    dct_results = {'dbase': [], 'query': [], 'atoms': [], 'charges': []}

    d_base = os.path.basename(d_path)
    q_base = os.path.basename(q_path)

    if verbose:
        start = time.time()
        sys.stdout.write('Processing %s/%s' % (d_base, q_base))
        sys.stdout.flush()

    cnt = 0
    for chunk in lazy_imap(data_processor=data_processor,
                           data_generator=zip(split_multimol2(d_path),
                                              split_multimol2(q_path)),
                           n_cpus=0):

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

    with open(output_file + '_charge.csv', 'w') as f1,\
            open(output_file + '_atomtype.csv', 'w') as f2:

        columns = PandasMol2().read_mol2(q_path).df['atom_name'].values
        f1.write('dbase,query,%s\n' % ','.join(columns))
        f2.write('dbase,query,%s\n' % ','.join(columns))
        for i in range(len(dct_results['dbase'])):
            s1 = '%s,%s,%s\n' % (dct_results['dbase'][i],
                                 dct_results['query'][i],
                                 ','.join(format(x, "10.2f")
                                          for x in dct_results['charges'][i]))

            f1.write(s1)
            s2 = '%s,%s,%s\n' % (dct_results['dbase'][i],
                                 dct_results['query'][i],
                                 ','.join(dct_results['atoms'][i]))
            f2.write(s2)

    if verbose:
        elapsed = time.time() - start
        n_molecules = cnt + 1
        sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                         (n_molecules, n_molecules / elapsed))
        sys.stdout.flush()


def main(input_dir, output_dir, verbose):
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
                       output_file=c)


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
    parser.add_argument('-d', '--max_distance',
                        type=float,
                        default=1.3,
                        help='Distance')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()
    THRESHOLD = args.max_distance

    main(input_dir=args.input,
         output_dir=args.output,
         verbose=args.verbose)
