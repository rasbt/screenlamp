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
import subprocess
import sys
import argparse
from biopandas.mol2.mol2_io import split_multimol2


def check_query(query_path):
    ids = [mol2[0] for mol2 in split_multimol2(query_path)]
    n_ids = len(ids)
    if n_ids > 1:
        n_unique_ids = len(set(ids))
        if n_unique_ids > 1:
            raise ValueError('Please Make sure that you only submit one'
                             ' molecule or, if you submit a multi-conformer'
                             ' query, that conformers of the molecule'
                             ' have all the same molecule ID labels.'
                             ' Found %d molecules and %d unique labels'
                             % (n_ids, n_unique_ids))


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


def run_shapeit(source_file, target_file, settings):

    prefix = ''.join(target_file.split('.mol2')[:-1])

    sys.stdout.write('Processing %s\n' % os.path.basename(source_file))
    sys.stdout.flush()

    if source_file.endswith('.gz'):
        sys.stdout.write('Shape-it does not support compressed files'
                         ' please decompress %s' %
                         os.path.basename(source_file))
        sys.stdout.flush()

    cmd = [EXECUTABLE,
           '--reference', QUERY_FILE,
           '--dbase', source_file,
           '--out', target_file,
           '--scores', prefix + '.rpt',
           '--noRef']

    if settings:
        for s in settings.split():
            s = s.strip()
            if s:
                cmd.append(s)

    print(' '.join(cmd))
    subprocess.call(cmd, stdout=subprocess.PIPE, bufsize=1)


def main(input_dir, output_dir, settings):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    check_query(QUERY_FILE)
    mol2_in_files = get_mol2_files(input_dir)
    mol2_out_files = [os.path.join(output_dir, os.path.basename(mol2))
                      for mol2 in mol2_in_files]

    for i, j in zip(mol2_in_files, mol2_out_files):
        run_shapeit(source_file=i,
                    target_file=j,
                    settings=settings)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Wrapper running Silicos-it Shape-it on one'
                        '\nor more database partitions.'
                        '\nFor more information about Shape-it, please see'
                        ' http://silicos-it.be.s3-website-eu-west-1.'
                        'amazonaws.com/software/shape-it/1.0.1/shape-it.html',
            epilog="""Example:
python overlay_molecules_shapeit.py\\
   --input database_conformers/\\
   --output shapeit_overlays/\\
   --executable 'shape-it'\\
   --query query.mol2\\
   --settings "--rankby Tanimoto""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Path to input directory containing the database'
                             '\nmolecules in `.mol2` and/or `.mol2.gz` format.'
                        )
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Directory path for writing'
                             ' the `.mol2`'
                             '\noverlays and Shape-it score/report (`.rpt`)'
                             ' files.')
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
    parser.add_argument('--executable',
                        type=str,
                        required=True,
                        help="""(Required.) The path or command for running
Slicos-it Shape-it on your system.""")
    parser.add_argument('--settings',
                        type=str,
                        default='--rankBy Tanimoto',
                        help='(Optional, default:" --rankBy Tanimoto")'
                             '\nshape-it settings to use.')

    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    QUERY_FILE = args.query
    EXECUTABLE = args.executable

    main(input_dir=args.input,
         output_dir=args.output,
         settings=args.settings)
