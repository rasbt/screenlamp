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
import pandas as pd
from biopandas.mol2 import split_multimol2
import tempfile
import pickle


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
                   sortby, separator, verbose, id_suffix, selection):

    if verbose:
        sys.stdout.write('Processing %s' % os.path.basename(inp_mol2_path))
        sys.stdout.flush()

    df = pd.read_table(report_path, usecols=['Name', 'ShapeQuery'] + sortby,
                       sep=separator)

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

    multiconf_query = False
    for idx, cont in enumerate(split_multimol2(query_path)):
        if idx >= 1:
            multiconf_query = True
            break

    cnt = -1

    if query_path.endswith('.gz'):
        for id_, cont in split_multimol2(query_path):
            cnt += 1
            cont = b''.join(cont).decode('utf-8').split('\n')
            if multiconf_query:
                mol_idx = '%s_%d' % (id_.decode('utf-8'), cnt)
            else:
                mol_idx = id_
            if mol_idx in query_names:
                if id_suffix:
                    cont[1] = mol_idx + '\n'
                query_mol2s[mol_idx] = ''.join(cont)

    else:
        for id_, cont in split_multimol2(query_path):
            cnt += 1
            if multiconf_query:
                mol_idx = '%s_%d' % (id_, cnt)
            else:
                mol_idx = id_
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
         sortby, separator, verbose, id_suffix, selection):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    inp_mol2_paths = get_mol2_files(input_dir)

    for mol2_path in inp_mol2_paths:
        base = os.path.basename(mol2_path)
        report_path = base.replace('.mol2', '.rpt').replace('_hits_', '_')
        report_path = os.path.join(os.path.dirname(mol2_path), report_path)
        read_and_write(mol2_path, report_path, output_dir, query_path,
                       sortby, separator, verbose, id_suffix, selection)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Sorts ROCS results by score and creates'
                        '\nseparate .mol2 files for the database'
                        ' and query molecules.',
            epilog="""Example:
python sort_rocs_mol2.py -i rocs_results/\\
   --output rocs_sorted/ --query mol.mol2\\
   --sortby TanimotoCombo,ColorTanimoto\\
   --selection "(TanimotoCombo >= 0.75) & (ColorTanimoto >= 0.1)" """,
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='(Required.) Input directory with results from a ROCS run.')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Directory path for writing the `.mol2` overlay'
                             '\nROCS status and ROCS report (`.rpt`) files')
    parser.add_argument('--query',
                        type=str,
                        required=True,
                        help='(Required.) Path to the query molecule'
                             '\nin `.mol2` and/or `.mol2.gz` format.'
                             '\nThe query molecule file could be a single'
                             '\nstructure of multiple-conformers of the same'
                             '\nstructure. If a multi-conformer file is'
                             '\nsubmitted, please make sure that all'
                             '\nconformers in the mol2 file have the same'
                             '\nmolecule ID/Name.')
    parser.add_argument('-s', '--sortby',
                        type=str,
                        default='TanimotoCombo,ColorTanimoto',
                        help='(Optional, default: `"TanimotoCombo,ColorTanimoto"`)'
                             '\nScore column(s) in ROCS report files that'
                             '\nthe structures should be sorted by.')
    parser.add_argument('--selection',
                        type=str,
                        default='(TanimotoCombo >= 1.0)'
                                ' & (ColorTanimoto >= 0.25)',
                        help='(Optional, default: `"(TanimotoCombo >= 1.0)) & (ColorTanimoto >= 0.25)"`)'
                             '\nSelection string to exclude molecules above'
                             '\nor below a certain score threshold. By default'
                             '\nall molecules with a ColorTanimoto score smaller than 0.25'
                             '\n and a TanimotoCombo score smaller than 1.0 will be disregarded.')
    parser.add_argument('--separator',
                        type=str,
                        default='\t',
                        help=('(Optional, default: `"\\t"`.) Column separator used\nin the input table.\n'
                              'Assumes tab-separated values by default.'))
    parser.add_argument('--id_suffix',
                        type=str,
                        default='False',
                        help='(Optional, default: `"False"`.)'
                             '\nIf `--id_suffix "True"`, a molecule ID suffix'
                             '\nwill be added to the query'
                             '\nmolecules in the order the ROCS query molecules'
                             '\nappear in a multi-conformer query file.'
                             '\nFor instance, if all query molecules are labeled "3kPZS",'
                             '\nthen the same structures in the output file are labeled'
                             '\n3kPZS_1, 3kPZS_2, ... Note that those modified conformer'
                             '\nwill correspond to the conformer names in the ROCS report'
                             '\ntables. However, they may appear in an unsorted order in'
                             '\nthe _query files, which are sorted by the overlay score'
                             '\nof the database molecules. For example, if the'
                             '\ndatabase molecule is called ZINC123_112, first'
                             '\nentry in the _query file that corresponds to *_dbase'
                             '\nfile may by labeled 3kPZS_11 if the 11th 3kPZS conformer'
                             '\nis the best match according to ROCS.')
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=1,
                        help='Verbosity level. If 0, does not print any'
                             ' output.'
                             '\nIf 1 (default), prints the file currently'
                             '\nprocessing.')

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

    for s in args.selection.split(' '):
        if s.startswith('(') and s[1:] not in args.sortby:
            raise ValueError('Selection columns are a subset of'
                             ' the --sortby columns. The column %s'
                             ' is currently not contained in the'
                             ' --sortby argument. Please add it '
                             'there to use this column as a '
                             'selection criterion.' % (s[1:]))

    main(input_dir=args.input, output_dir=args.output, query_path=args.query,
         sortby=sortby,
         verbose=args.verbose,
         separator=args.separator,
         id_suffix=id_suffix,
         selection=args.selection)
