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
import pandas as pd
import gzip
import time
from biopandas.mol2 import split_multimol2


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
                                                   os.path.basename(c_in)))
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

            if not os.path.exists(input_mol2_path_query)\
                    and os.path.exists(input_mol2_path_query + '.gz'):
                input_mol2_path_query += '.gz'
            if not os.path.exists(input_mol2_path_dbase)\
                    and os.path.exists(input_mol2_path_dbase + '.gz'):
                input_mol2_path_dbase += '.gz'

            output_mol2_path_query = os.path.join(output_dir,
                                                  os.path.basename(
                                                   c_out).replace(
                                                   '_charge.tsv',
                                                   '_query.mol2'))
            output_mol2_path_dbase = output_mol2_path_query.replace(
                                     '_query.mol2', '_dbase.mol2')

            if input_mol2_path_query.endswith('.gz'):
                output_mol2_path_query += '.gz'
                query_write_mode = 'wb'
                query_open_file = gzip.open
            else:
                query_write_mode = 'w'
                query_open_file = open
            if input_mol2_path_dbase.endswith('.gz'):
                output_mol2_path_dbase += '.gz'
                dbase_write_mode = 'wb'
                dbase_open_file = gzip.open
            else:
                dbase_write_mode = 'w'
                dbase_open_file = open

            with query_open_file(output_mol2_path_query, query_write_mode) as opq,\
                    dbase_open_file(output_mol2_path_dbase, dbase_write_mode) as opd:
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

                    if query_write_mode == 'wb':
                        opq.write(b''.join(mol2_q_cont))
                    else:
                        opq.write(''.join(mol2_q_cont))

                    if dbase_write_mode == 'wb':
                        opd.write(b''.join(mol2_d_cont))
                    else:
                        opd.write(''.join(mol2_d_cont))

        if verbose:
            elapsed = time.time() - start
            n_molecules = mol2_cnt
            sys.stdout.write(' | scanned %d molecules | %d mol/sec\n' %
                             (n_molecules, n_molecules / elapsed))
            sys.stdout.flush()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Selects molecules with certain functional group matching patterns after functional group matching.',
            epilog="""Example:
python funcgroup_matching_selection.py\\
  --input 07_fgroup_matching_tables # generated via funcgroup_matching.py\\
  --input_mol2 06_rocs_overlays_sorted # generated via sort_rocs_mol2.py\\
  --output 08_funcgroup_selection\\
  --atomtype_selection "((S1 == 'S.3') | (S1 == 'S.o2')) --> (O2 == 'O.2')"\\
  --charge_selection FGROUP_CHARGE "((S1 >= 1.0)) --> (O2 <= -0.5)" """,
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help=('(Required.) Input directory with input `.tsv` tables (functional group files'
                              ' generated via `funcgroup_matching.py`).'))
    parser.add_argument('--input_mol2',
                        type=str,
                        help=('(Optional.) Input directory with input `.mol2` structures (ROCS overlays'
                              '\ngenerated via `sort_rocs_mol2.py`). If provided, the MOL2 structures'
                              '\ncorresponding to the selected matches will be extracted from the'
                              '\ninput_mol2 directory and written to the output directory for visual inspection,'
                              '\nfor example, using PyMOL.'))
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Directory for writing the output files.')
    parser.add_argument('--atomtype_selection',
                        type=str,
                        default="",
                        help="""(Optional, default="") Selection condition for the atom types.
For example, the following selection query will make a selection based on
matching 2 atoms in the reference molecule, S1 and O2:
"((S1 == 'S.3') | (S1 == 'S.o2')) --> (O2 == 'O.2')".
Here, S1 can either match an S.3 or an S.o2 atom in the database molecule.
The second atom, O2, must match an atom of type O.2.""")
    parser.add_argument('--charge_selection',
                        type=str,
                        default="",
                        help="""(Optional, default="") Selection condition for the atom charges.
For example, the following selection query will make a selection based on
matching the charges in 2 atoms in the reference molecule, S1 and O2:
"((S1 >= 1.0)) --> (O2 <= -0.5)".
Here, the atom that matches S1 has to have a positive charge, 1 or greater. The charge
matching the second atom, O2, must be (partially) negative (-0.5 or smaller).""")
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
         output_dir=args.output,
         atomtype_selection=args.atomtype_selection,
         charge_selection=args.charge_selection,
         input_mol2=args.input_mol2,
         verbose=args.verbose)