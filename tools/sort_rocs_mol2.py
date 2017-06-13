import os
import argparse
import sys
import time
import pandas as pd
from biopandas.mol2 import split_multimol2
import tempfile
import pickle

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


def parse_selection_string(s, df_name='df'):
    return s.replace('(', '(%s.' % df_name)


def read_and_write(inp_mol2_path, report_path, output_dir, query_path,
                   sortby, column_seperator, verbose, id_suffix, selection):

    if verbose:
        sys.stdout.write('Processing %s' % os.path.basename(inp_mol2_path))
        sys.stdout.flush()

    df = pd.read_table(report_path, usecols=['Name', 'ShapeQuery'] + sortby,
                       sep=column_seperator)

    if sortby:
        df.sort_values(sortby, inplace=True, ascending=False)

    if selection:
        selection_str = parse_selection_string(selection, df_name='df')
        mask = pd.eval(selection_str)
        df = df[mask]

    dbase_query_pairs = [(d, q) for d, q in
                         zip(df['Name'].values, df['ShapeQuery'].values)]
    query_names = {q for q in df['ShapeQuery'].values}

    query_mol2s = {}

    cnt = -1
    for id_, cont in split_multimol2(query_path):
        cnt += 1
        mol_idx = '%s_%d' % (id_, cnt)
        if mol_idx in query_names:
            if id_suffix:
                cont[1] = mol_idx + '\n'
            query_mol2s[mol_idx] = ''.join(cont)

    out_path_base = os.path.join(output_dir, os.path.basename(inp_mol2_path)
                                 .split('.mol2')[0])
    out_path_q = '%s_%s' % (out_path_base, 'query.mol2')
    out_path_d = '%s_%s' % (out_path_base, 'dbase.mol2')

    with tempfile.TemporaryDirectory() as tmpdirname:
        for id_, cont in split_multimol2(inp_mol2_path):
            if id_:
                tmp_path = os.path.join(tmpdirname, id_)
                with open(tmp_path, 'wb') as f:
                    pickle.dump(''.join(cont), f)

        with open(out_path_d, 'w') as dof,\
                open(out_path_q, 'w') as qof:

            if verbose:
                start = time.time()

            cnt = 0
            for d, q in dbase_query_pairs:
                cnt += 1
                qof.write(query_mol2s[q])
                with open(os.path.join(tmpdirname, d), 'rb') as pkl:
                    pkl_cont = pickle.load(pkl)
                    dof.write(pkl_cont)

    if verbose:
        elapsed = time.time() - start
        n_molecules = cnt + 1
        sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                         (n_molecules, n_molecules / elapsed))
        sys.stdout.flush()


def main(input_dir, output_dir, query_path,
         sortby, column_seperator, verbose, id_suffix, selection):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    inp_mol2_paths = get_mol2_files(input_dir)

    for mol2_path in inp_mol2_paths:
        base = os.path.basename(mol2_path)
        report_path = base.replace('.mol2', '.rpt').replace('_hits_', '_')
        report_path = os.path.join(os.path.dirname(mol2_path), report_path)
        read_and_write(mol2_path, report_path, output_dir, query_path,
                       sortby, column_seperator, verbose, id_suffix, selection)


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
    parser.add_argument('-q', '--query',
                        required=True,
                        type=str,
                        help='Query molecule file')
    parser.add_argument('-s', '--sortby',
                        type=str,
                        default='TanimotoCombo,ColorTanimoto',
                        help='')
    parser.add_argument('--selection',
                        type=str,
                        default='(TanimotoCombo >= 1.0)'
                                ' & (ColorTanimoto >= 0.25)',
                        help='')
    parser.add_argument('--column_seperator',
                        type=str,
                        default='\t',
                        help='')
    parser.add_argument('--id_suffix',
                        type=str,
                        default='False',
                        help='')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             ' If 1 (default), prints the file currently'
                             ' processing.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    if args.id_suffix.lower() in {'false', 'f', 'no', 'n'}:
        id_suffix = False
    elif args.id_suffix.lower() in {'true', 't', 'yes', 'y'}:
        id_suffix = True
    else:
        raise ValueError('--id_suffix must be true or false. Got %s' %
                         args.id_suffix)

    sortby = [s.strip() for s in args.sortby.split(',')]
    main(input_dir=args.input, output_dir=args.output, query_path=args.query,
         sortby=sortby, 
         verbose=args.verbose,
         column_seperator=args.column_seperator,
         id_suffix=id_suffix,
         selection=args.selection)
