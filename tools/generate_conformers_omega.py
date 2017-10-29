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
from multiprocessing import cpu_count


def get_num_cpus(n_cpus):
    if not n_cpus:
        n_cpus = cpu_count()
    elif n_cpus < 0:
        n_cpus = cpu_count() - n_cpus
    return n_cpus


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


def run_omega(source_file, target_file, n_processes, settings):

    prefix = ''.join(target_file.split('.mol2')[:-1])

    sys.stdout.write('Processing %s\n' % source_file)
    sys.stdout.flush()

    cmd = [EXECUTABLE,
           '-in', source_file,
           '-out', target_file,
           '-prefix', prefix,
           '-mpi_np', str(n_processes)]
    if settings:
        for s in settings.split():
            s = s.strip()
            if s:
                cmd.append(s)

    subprocess.call(cmd, stdout=subprocess.PIPE, bufsize=1)


def main(input_dir, output_dir, n_processes, settings):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    mol2_in_files = get_mol2_files(input_dir)
    mol2_out_files = [os.path.join(output_dir, os.path.basename(mol2))
                      for mol2 in mol2_in_files]

    n_processes = get_num_cpus(n_processes)

    for i, j in zip(mol2_in_files, mol2_out_files):
        run_omega(source_file=i,
                  target_file=j,
                  n_processes=n_processes,
                  settings=settings)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Wrapper running OpenEye OMEGA on one'
                        '\nor more database partitions.',
            epilog="""Example:
python generate_conformers_omega.py\\
   --input dbase_mol2\\
   --output dbase_conformers/\\
   --executable /.../omega2-2.5.1.4\\
   --processes 0""",
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
OpenEye OMEGA2 on your system.""")
    parser.add_argument('--settings',
                        type=str,
                        default='-maxconfs 200 -warts false -progress percent',
                        help='(Optional.) OMEGA settings to use.')
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

    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    EXECUTABLE = args.executable

    main(input_dir=args.input,
         output_dir=args.output,
         n_processes=args.processes,
         settings=args.settings)
