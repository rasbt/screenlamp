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


def read_idfile(id_file_path):
    with open(id_file_path, 'r') as f:
        ids = {line.strip() for line in f if not line.startswith('#')}
    return ids


def main(id_file_path_1, id_file_path_2, output_path):

    cache = set()
    with open(output_path, 'w') as ofile:
        with open(id_file_path_1, 'r') as f1:
            for line in f1:
                line = line.strip()
                if not line.startswith('#') and line not in cache:
                    ofile.write('%s\n' % line)
                    cache.add(line)
        with open(id_file_path_2, 'r') as f2:
            for line in f2:
                line = line.strip()
                if not line.startswith('#') and line not in cache:
                    ofile.write('%s\n' % line)
                    cache.add(line)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description="""Merges two Molecule ID files
(e.g., created via `datatable_to_id.py`, `funcgroup_presence_to_id.py`
 or `mol2_to_id.py`) into a single ID file
 while preventing duplicate entries.""",
            epilog="""Example:
python merge_id_files.py\\
   --input1 mol2s_1.txt\\
   --input2 mol2s_2.txt\\
   --output merged.txt""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i1', '--input1',
                        type=str,
                        required=True,
                        help='(Required.) Input ID file that contains molecule'
                             '\nIDs (one ID per line).')
    parser.add_argument('-i2', '--input2',
                        type=str,
                        required=True,
                        help='(Required.) Input ID file that contains molecule'
                             '\nIDs (one ID per line).')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='(Required.) Path to the output ID file.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(id_file_path_1=args.input1,
         id_file_path_2=args.input2,
         output_path=args.output)
