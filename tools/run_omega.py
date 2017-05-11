import os
import subprocess
import sys
import argparse
from multiprocessing import Pool
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


def run_omega(source_file, target_file):

    prefix = ''.join(target_file.split('.mol2')[:-1])

    sys.stdout.write('Processing %s\n' % source_file)
    sys.stdout.flush()

    cmd = [EXECUTABLE,
           '-in', source_file,
           '-out', target_file,
           '-prefix', prefix,
           '-maxconfs', '200',
           '-warts', 'false']
    
    subprocess.call(cmd, stdout=subprocess.PIPE, bufsize=1)


def subprocess_runner(source_files, target_files, n_processes, func):

    pool = Pool(processes=n_processes)

    arguments = [(x, y) for x, y in zip(source_files, target_files)]

    _ = [pool.apply_async(func, args=(x, y)) for x, y in arguments]
    pool.close()
    pool.join()


def main(input_dir, output_dir, n_processes):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    mol2_in_files = get_mol2_files(input_dir)
    mol2_out_files = [os.path.join(output_dir, os.path.basename(mol2))
                      for mol2 in mol2_in_files]
    n_processes = get_num_cpus(n_processes)
    subprocess_runner(source_files=mol2_in_files,
                      target_files=mol2_out_files,
                      n_processes=n_processes,
                      func=run_omega)


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
    parser.add_argument('--executable',
                        type=str,
                        help='Omega2 executable')
    parser.add_argument('-p', '--processes',
                        type=int,
                        default=1,
                        help='Number of processes to run in parallel.'
                             ' Uses all CPUs if 0')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    EXECUTABLE = args.executable

    main(input_dir=args.input,
         output_dir=args.output,
         n_processes=args.processes)
