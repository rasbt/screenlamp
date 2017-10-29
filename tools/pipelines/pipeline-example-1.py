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
                    help='Start the pipeline at a particular step')

parser.add_argument('-i', '--incremental',
                    type=str,
                    required=False,
                    default='false',
                    help='incremental mode. If enabled, stops before each step'
                    ' to ask the user to continue')

args = parser.parse_args()
start_at = args.start_at_step
config_path = args.config_file

print(args.incremental)
if args.incremental.lower() not in {'true', 'false'}:
    raise AttributeError('incremental must be true or false')
if args.incremental == 'true':
    incremental = True
else:
    incremental = False

with open(config_path, 'r') as stream:
    ymldct = yaml.load(stream)

PROJECT_PATH = ymldct['general settings']['project output directory']
SCREENLAMP_TOOLS_DIR = ymldct['general settings']['screenlamp tools directory']
INPUT_MOL2_PATH = ymldct['general settings']['input mol2 directory']
N_CPUS = str(ymldct['general settings']['number of cpus'])
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
ROCS_RANKBY = ymldct['ROCS settings']['ROCS run rankby']
ROCS_SORTBY = ymldct['ROCS settings']['ROCS results sort by']
ROCS_THRESHOLD = ymldct['ROCS settings']['ROCS score threshold']
QUERY_PATH = ymldct['ROCS settings']['query molecule path']

FGROUP_MATCH_DISTANCE = str(ymldct['functional group matching '
                                   'selection settings'][
                                   'maximum pairwise atom distance'])

WRITE_MATCH_OVERLAYS = False
if ymldct['functional group match selection settings']['write mol2 files'] in (
      'true', True):
    WRITE_MATCH_OVERLAYS = True
FGROUP_ATOMTYPE = ymldct['functional group match selection settings'][
                         'atomtype selection keys']
FGROUP_CHARGE = ymldct['functional group match selection settings'][
                       'charge selection keys']

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

    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
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
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\n')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
           '--input', INPUT_MOL2_PATH,
           '--id_file', os.path.join(PROJECT_PATH, '01_ids_from_database.txt'),
           '--output', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
           '--includelist', 'True']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s')]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)

###############################################################################

if start_at <= 2:
    s = """

################################################
Step 02: PREFILTER BY FUNCTIONAL GROUP PRESENCE
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR,
                                  'funcgroup_presence_to_id.py'),
           '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
           '--output', os.path.join(PROJECT_PATH,
                                    '02_fgroup-presence_mol2ids.txt'),
           '--selection', FUNCTIONAL_GROUP_PRESENCE,
           '--processes', N_CPUS]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\n')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
           '--id_file', os.path.join(PROJECT_PATH,
                                     '02_fgroup-presence_mol2ids.txt'),
           '--output', os.path.join(PROJECT_PATH, '02_fgroup-presence_mol2s'),
           '--includelist', 'True']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '02_fgroup-presence_mol2s')]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
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
           '--input', os.path.join(PROJECT_PATH, '02_fgroup-presence_mol2s'),
           '--output', os.path.join(PROJECT_PATH,
                                    '03_fgroup_distance_mol2ids.txt'),
           '--selection', FUNCTIONAL_GROUP_DISTANCE_SELECTION,
           '--distance', FUNCTIONAL_GROUP_DISTANCE,
           '--processes', N_CPUS]

    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\n')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '02_fgroup-presence_mol2s'),
           '--id_file', os.path.join(PROJECT_PATH,
                                     '03_fgroup_distance_mol2ids.txt'),
           '--output', os.path.join(PROJECT_PATH,
                                    '03_fgroup_distance_mol2s'),
           '--includelist', 'True']

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH,
                                   '03_fgroup_distance_mol2s')]

    print('Running command:\n%s\n' % ' '.join(cmd))

    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)

###############################################################################

if start_at <= 4:
    s = """

################################################
Step 04: OMEGA conformers
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'generate_conformers_omega.py'),
           '--input', os.path.join(PROJECT_PATH,
                                   '03_fgroup_distance_mol2s'),
           '--output', os.path.join(PROJECT_PATH, '04_omega_conformers'),
           '--executable', OMEGA_EXECUTABLE,
           '--processes', N_CPUS]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)
    print('\n\nSELECTED MOL2s:')

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '04_omega_conformers')]

    print('Running command:\n%s\n' % ' '.join(cmd))

    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)

###############################################################################

if start_at <= 5:

    s = """

################################################
Step 05: ROCS OVERLAYS
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'overlay_molecules_rocs.py'),
           '--input', os.path.join(PROJECT_PATH, '04_omega_conformers'),
           '--output', os.path.join(PROJECT_PATH, '05_rocs_overlays'),
           '--executable', ROCS_EXECUTABLE,
           '--query', QUERY_PATH,
           '--settings', ('-rankby %s -maxhits 0'
                          ' -besthits 0 -progress percent' %
                          ROCS_RANKBY),
           '--processes', N_CPUS]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '05_rocs_overlays')]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)


###############################################################################

if start_at <= 6:

    s = """

################################################
Step 06: SORT ROCS OVERLAYS
################################################
    """
    print(s)

    cmd = ['python',  os.path.join(SCREENLAMP_TOOLS_DIR, 'sort_rocs_mol2.py'),
           '--input', os.path.join(PROJECT_PATH, '05_rocs_overlays'),
           '--output', os.path.join(PROJECT_PATH, '06_rocs_overlays_sorted'),
           '--query', QUERY_PATH,
           '--sortby', ROCS_SORTBY,
           '--selection', ROCS_THRESHOLD]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)

###############################################################################

if start_at <= 7:

    s = """

################################################
Step 07: MATCHING FUNCTIONAL GROUPS
################################################
    """
    print(s)

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR,
                                  'funcgroup_matching.py'),
           '--input', os.path.join(PROJECT_PATH, '06_rocs_overlays_sorted'),
           '--output', os.path.join(PROJECT_PATH, '07_funcgroup_matching'),
           '--max_distance', FGROUP_MATCH_DISTANCE,
           '--processes', N_CPUS]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)

###############################################################################

if start_at <= 8:

    s = """

################################################
Step 08: SELECTING FUNCTIONAL GROUP MATCHES
################################################
    """
    print(s)

    if WRITE_MATCH_OVERLAYS:
        in_path = os.path.join(PROJECT_PATH, '06_rocs_overlays_sorted')
    else:
        in_path = ''

    cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR,
                                  'funcgroup_matching_selection.py'),
           '--input', os.path.join(PROJECT_PATH, '07_funcgroup_matching'),
           '--output', os.path.join(PROJECT_PATH, '08_funcgroup_selection'),
           '--atomtype_selection', FGROUP_ATOMTYPE,
           '--charge_selection', FGROUP_CHARGE,
           '--input_mol2', in_path]

    print('Running command:\n%s\n' % ' '.join(cmd))
    if incremental:
        input('Press Enter to proceed or CTRL+C to quit')
    subprocess.call(cmd)