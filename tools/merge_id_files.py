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
            description='Placeholder.',
            epilog='Example: python mol2_to_id.py -i mol2_dir -o ids.txt\n',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--input1',
                        type=str,
                        required=True,
                        help='Input ID file that contains molecule'
                             'IDs (one ID per line)')
    parser.add_argument('--input2',
                        type=str,
                        required=True,
                        help='Input ID file that contains molecule'
                             'IDs (one ID per line)')
    parser.add_argument('--output',
                        type=str,
                        required=True,
                        help='Path to the output ID file.')

    parser.add_argument('--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    main(id_file_path_1=args.input1,
         id_file_path_2=args.input2,
         output_path=args.output)
