import argparse
import os
import sys
import pandas as pd
import time
from biopandas.mol2 import split_multimol2

# make mol2.gz compatible


def get_tsv_pairs(all_tsv):
    a_list, c_list = [], []
    for a in all_tsv:
        if a.endswith('_atomtype.tsv'):
            a_list.append(a)
        elif a.endswith('_charge.tsv'):
            c_list.append(a)
    if len(a_list) != len(c_list):
        raise ValueError('The input directory contains an unequal number of'
                         '*_atomtype.tsv* and *_charge.tsv* files.')
    return a_list, c_list


def parse_selection_string(s, columns, df_name='df'):

    for c in columns:
        if c in s:
            s = s.replace(c, '%s.%s' % (df_name, c))
    s = s.replace(' --> ', '-->').split('-->')
    s = ['%s[%s]' % (df_name, sub) for sub in s]
    return s


def main(input_dir, output_dir, atomtype_selection, charge_selection, 
         input_mol2, verbose):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    all_tsv_base = [f for f in os.listdir(input_dir) if f.endswith('.tsv')]
    all_tsv_full = [os.path.join(input_dir, f) for f in all_tsv_base]
    a_inlist, c_inlist = get_tsv_pairs(all_tsv_full)
    a_outlist, c_outlist = get_tsv_pairs(all_tsv_base)
    a_outlist = [os.path.join(output_dir, f) for f in a_outlist]
    c_outlist = [os.path.join(output_dir, f) for f in c_outlist]

    for a_in, a_out, c_in, c_out in zip(a_inlist, a_outlist,
                                        c_inlist, c_outlist):

        if verbose:
            start = time.time()
            sys.stdout.write('Processing %s/%s' % (os.path.basename(a_in),
                                                   os.path.basename(a_in)))
            sys.stdout.flush()

        df_charge = pd.read_table(c_in, sep='\t')
        for c in df_charge.columns[2:]:
            df_charge[c] = pd.to_numeric(df_charge[c])
        df_atom = pd.read_table(a_in, sep='\t')
        mol2_cnt = df_atom.shape[0]

        if atomtype_selection:
            atom_sele = parse_selection_string(s=atomtype_selection,
                                               columns=df_atom.columns,
                                               df_name='df_atom')

            for sele in atom_sele:
                df_atom = pd.eval(sele)

        if charge_selection:
            charge_sele = parse_selection_string(s=charge_selection,
                                                 columns=df_charge.columns,
                                                 df_name='df_charge')

            for sele in charge_sele:
                df_charge = pd.eval(sele)

        selection_indices = set(df_charge.index).intersection(
                            set(df_atom.index))
        selection_indices = sorted(list(selection_indices))

        df_atom.ix[selection_indices].to_csv(a_out, sep='\t')
        df_charge.ix[selection_indices].to_csv(c_out, sep='\t')

        if input_mol2:
            input_mol2_path_query = os.path.join(input_mol2, os.path.basename(
                                    c_out).replace('_charge.tsv',
                                                   '_query.mol2'))
            input_mol2_path_dbase = input_mol2_path_query.replace(
                                    '_query.mol2', '_dbase.mol2')

            output_mol2_path_query = os.path.join(output_dir,
                                                  os.path.basename(
                                                   c_out).replace(
                                                   '_charge.tsv',
                                                   '_query.mol2'))
            output_mol2_path_dbase = output_mol2_path_query.replace(
                                     '_query.mol2', '_dbase.mol2')

            with open(output_mol2_path_query, 'w') as opq, open(
                    output_mol2_path_dbase, 'w') as opd:
                for i in selection_indices:

                    mol2_q_cont = ('DID NOT FIND %s\n'
                                   % (df_atom.ix[i]['query']))

                    mol2_d_cont = ('DID NOT FIND %s\n'
                                   % (df_atom.ix[i]['dbase']))

                    for idx, mol2 in enumerate(split_multimol2(
                            input_mol2_path_query)):
                        if idx == i:
                            mol2_q_cont = mol2[1]
                            break

                    for idx, mol2 in enumerate(split_multimol2(
                            input_mol2_path_dbase)):
                        if idx == i:
                            mol2_d_cont = mol2[1]
                            break

                    opq.write(''.join(mol2_q_cont))
                    opd.write(''.join(mol2_d_cont))

        if verbose:
            elapsed = time.time() - start
            n_molecules = mol2_cnt
            sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                             (n_molecules, n_molecules / elapsed))
            sys.stdout.flush()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='A command line tool for filtering mol2 files.',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory with input tsv files')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Directory for writing the output files')
    parser.add_argument('--atomtype_selection',
                        type=str,
                        default='',
                        help='Directory for writing the output files')
    parser.add_argument('--charge_selection',
                        type=str,
                        default='',
                        help='Directory for writing the output files')
    parser.add_argument('--input_mol2',
                        type=str,
                        default='',
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

    main(input_dir=args.input,
         output_dir=args.output,
         atomtype_selection=args.atomtype_selection,
         charge_selection=args.charge_selection,
         input_mol2=args.input_mol2,
         verbose=args.verbose)