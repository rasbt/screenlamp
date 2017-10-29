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


def run_obabel(source_file, target_file, settings):

    sys.stdout.write('Processing %s\n' % source_file)
    sys.stdout.flush()

    cmd = [EXECUTABLE,
           source_file,
           '-O', target_file,
           '--original',
           '--confab']
    if settings:
        for s in settings.split():
            s = s.strip()
            if s:
                cmd.append(s)

    if source_file.endswith('.gz'):
        cmd.extend(['-zin', '-z'])
    prefix = ''.join(target_file.split('.mol2')[:-1])

    with open(prefix + '.log', 'wb') as out, \
            open(prefix + '.err', 'wb') as err:

        subprocess.call(cmd, bufsize=1, stdout=out, stderr=err)


def main(input_dir, output_dir, settings):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    mol2_in_files = get_mol2_files(input_dir)
    mol2_out_files = [os.path.join(output_dir, os.path.basename(mol2))
                      for mol2 in mol2_in_files]

    for i, j in zip(mol2_in_files, mol2_out_files):
        run_obabel(source_file=i,
                   target_file=j,
                   settings=settings)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Wrapper running OpenBabel Confab on one'
                        '\nor more database partitions.'
                        ' Please see'
                        '\nhttp://open-babel.readthedocs.io/en/latest/'
                        '3DStructureGen/multipleconformers.html'
                        '\nif you want to learn more about OpenBabel Confab.',
            epilog="""Example:
python generate_conformers_obabel.py\\
   --input dbase_mol2/\\
   --output dbase_conformers/\\
   --executable /.../obabel""",
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input directory with `.mol2`'
                             ' and `.mol2.gz` files.')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Directory for writing the output files.')
    parser.add_argument('--executable',
                        type=str,
                        required=True,
                        help="""(Required.) The path or command for running
OpenBabel Confab on your system.""")
    parser.add_argument('--settings',
                        type=str,
                        default='--conf 200 --ecutoff 50''--rcutoff 0.5',
                        help='(Optional.) OpenBabel settings to use.')

    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    EXECUTABLE = args.executable

    main(input_dir=args.input,
         output_dir=args.output,
         settings=args.settings)
