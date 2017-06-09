# Sebastian Raschka 2017
#
# `screenlamp` is a Python toolkit for using
# filters and pipelines for hypothesis-driven
# virtual screening.
#
# Copyright (C) 2017 Michigan State University
# License: MIT
#
# SiteInterlock was developed in the
# Protein Structural Analysis & Design Laboratory
# (http://www.kuhnlab.bmb.msu.edu)
#
# Author: Sebastian Raschka <http://sebastianraschka.com>
# Author email: mail@sebastianraschka.com

import subprocess
import os
import argparse
import yaml


###############################################################################

parser = argparse.ArgumentParser(
        description='An example screenlamp pipeline ... [placeholder].',
        formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-c', '--config_file',
                    type=str,
                    required=True,
                    default=0,
                    help='Path to the pipeline configuration file')

parser.add_argument('-s', '--start_at_step',
                    type=int,
                    required=False,
                    default=0,
                    help='Placeholder')

parser.add_argument('-i', '--interactive',
                    type=str,
                    required=False,
                    default='false',
                    help='Interactive mode. If enabled, stops before each step'
                    ' to ask the user to continue')

args = parser.parse_args()
start_at = args.start_at_step
config_path = args.config_file

print(args.interactive)
if args.interactive.lower() not in {'true', 'false'}:
    raise AttributeError('interactive must be true or false')
if args.interactive == 'true':
    interactive = True
else:
    interactive = False

with open(config_path, 'r') as stream:
    ymldct = yaml.load(stream)

PROJECT_PATH = ymldct['general settings']['project output directory']
SCREENLAMP_TOOLS_DIR = ymldct['general settings']['screenlamp tools directory']
INPUT_MOL2_PATH = ymldct['general settings']['input mol2 directory']
DATATABLE_PATH = ymldct['molecule property filter settings']['datatable path']
DATATABLE_FILTER = ymldct['molecule property filter settings']['column filter']
FUNCTIONAL_GROUP_PRESENCE = ymldct[
    'functional group presence filter settings']['selection key']
FUNCTIONAL_GROUP_DISTANCE_SELECTION = ymldct[
    'functional group distance filter settings']['selection key']
FUNCTIONAL_GROUP_DISTANCE = ymldct[
    'functional group distance filter settings']['distance']
OMEGA_EXECUTABLE = ymldct['OMEGA settings']['OMEGA executable']
ROCS_EXECUTABLE = ymldct['ROCS settings']['ROCS executable']
ROCS_SORTBY = ymldct['ROCS settings']['ROCS sort by']
QUERY_PATH = ymldct['ROCS settings']['query molecule path']

if not os.path.exists(PROJECT_PATH):
    os.makedirs(PROJECT_PATH)

###############################################################################

if start_at <= 0:
    s = """

################################################
COUNT MOLECULES IN DATATABLE_PATH
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', INPUT_MOL2_PATH]

    print('Running command:\n%s\n' % ' '.join(cmd))

    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

###############################################################################

if start_at <= 1:
    s = """

################################################
Step 01: SELECT MOLECULES FROM DATA TABLE
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'datatable_to_id.py'),
           '--input', DATATABLE_PATH,
           '--output', os.path.join(PROJECT_PATH, '01_ids_from_database.txt'),
           '--id_column', 'ZINC_ID',
           '--selection', DATATABLE_FILTER]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\n')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
           '--input', INPUT_MOL2_PATH,
           '--id_file', os.path.join(PROJECT_PATH, '01_ids_from_database.txt'),
           '--output', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
           '--whitelist', 'True']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s')]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

###############################################################################

if start_at <= 2:
    s = """

################################################
Step 02: PREFILTER BY FUNCTIONAL GROUP PRESENCE
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'funcgroup_to_id.py'),
           '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
           '--output', os.path.join(PROJECT_PATH,
                                    '02_3keto-and-sulfur-mol2ids.txt'),
           '--selection', FUNCTIONAL_GROUP_PRESENCE,
           '--processes', '0']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\n')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
           '--id_file', os.path.join(PROJECT_PATH,
                                     '02_3keto-and-sulfur-mol2ids.txt'),
           '--output', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s'),
           '--whitelist', 'True']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s')]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

###############################################################################

if start_at <= 3:
    s = """

################################################
Step 03: PREFILTER BY FUNCTIONAL GROUP DISTANCE
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR,
                                  'funcgroup_distance_to_id.py'),
           '--input', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s'),
           '--output', os.path.join(PROJECT_PATH,
                                    '03_3keto-and-sulfur-13-20A_mol2ids.txt'),
           '--selection', FUNCTIONAL_GROUP_DISTANCE_SELECTION,
           '--distance', FUNCTIONAL_GROUP_DISTANCE,
           '--processes', '0']

    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\n')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s'),
           '--id_file', os.path.join(PROJECT_PATH,
                                     '03_3keto-and-sulfur-13-20A_mol2ids.txt'),
           '--output', os.path.join(PROJECT_PATH,
                                    '03_3keto-and-sulfur-13-20A_mol2s'),
           '--whitelist', 'True']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH,
                                   '03_3keto-and-sulfur-13-20A_mol2s')]

    print('Running command:\n%s\n' % ' '.join(cmd))

    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

###############################################################################

if start_at <= 4:
    s = """

################################################
Step 04: OMEGA conformers
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'run_omega.py'),
           '--input', os.path.join(PROJECT_PATH,
                                   '03_3keto-and-sulfur-13-20A_mol2s'),
           '--output', os.path.join(PROJECT_PATH, '04_omega_conformers'),
           '--executable', OMEGA_EXECUTABLE,
           '--processes', '0']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '04_omega_conformers')]

    print('Running command:\n%s\n' % ' '.join(cmd))

    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

###############################################################################

if start_at <= 5:

    s = """

################################################
Step 05: ROCS OVERLAYS
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'run_rocs.py'),
           '--input', os.path.join(PROJECT_PATH, '04_omega_conformers'),
           '--output', os.path.join(PROJECT_PATH, '05_rocs_overlays'),
           '--executable', ROCS_EXECUTABLE,
           '--query', QUERY_PATH,
           '--settings', ('-rankby %s -maxhits 0'
                          ' -besthits 0 -progress percent' %
                          ROCS_SORTBY),
           '--processes', '0']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '05_rocs_overlays')]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)

    cmd = ['python',  os.path.join(SCREENLAMP_TOOLS_DIR, 'sort_rocs_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '05_rocs_overlays'),
           '--output', os.path.join(PROJECT_PATH, '05_rocs_overlays_sorted'),
           '--query', QUERY_PATH,
           '--sortby', ROCS_SORTBY]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if interactive:
        input('Press Enter to proceed')
    subprocess.call(cmd)
