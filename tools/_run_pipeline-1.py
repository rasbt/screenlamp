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

PROJECT_PATH = '/Users/sebastian/Desktop/screenlamp_pipe'
SCREENLAMP_TOOLS_DIR = '/Users/sebastian/code/screenlamp/tools'
INPUT_MOL2_PATH = ('/Users/sebastian/code/screenlamp/docs/sources/workflow/'
                   'example_1/dataset/mol2')
DATATABLE_PATH = ('/Users/sebastian/code/screenlamp/docs/sources/workflow/'
                  'example_1/dataset/tables/3_prop.xls')
DATATABLE_FILTER = "(NRB <= 7) & (MWT >= 200)"
FUNCTIONAL_GROUP_PRESENCE = "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"
FUNCTIONAL_GROUP_DISTANCE_SELECTION = "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"
FUNCTIONAL_GROUP_DISTANCE = "13-20"
OMEGA_EXECUTABLE = '/Applications/OMEGA 2.5.1.4.app/Contents/MacOS/omega2-2.5.1.4'
ROCS_EXECUTABLE = '/Applications/ROCS 3.2.1.4.app/Contents/MacOS/rocs-3.2.1.4'
QUERY_PATH = ('/Users/sebastian/code/screenlamp/docs/sources/workflow/'
              'example_1/dataset/query/3kpzs_conf_subset_nowarts.mol2')

if not os.path.exists(PROJECT_PATH):
    os.mkdir(PROJECT_PATH)


##############################################################################

s = """

################################################
COUNT MOLECULES IN DATATABLE_PATH
################################################
"""
print(s)

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
       '--input', INPUT_MOL2_PATH]

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)

##############################################################################

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
subprocess.call(cmd)
print('\n\n')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
       '--input', INPUT_MOL2_PATH,
       '--id_file', os.path.join(PROJECT_PATH, '01_ids_from_database.txt'),
       '--output', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
       '--whitelist', 'True']

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)
print('\n\nSELECTED MOL2s:')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
       '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s')]

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)


##############################################################################

s = """

################################################
Step 02: PREFILTER BY FUNCTIONAL GROUP PRESENCE
################################################
"""
print(s)


cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'funcgroup_to_id.py'),
       '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
       '--output', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2ids.txt'),
       '--selection', FUNCTIONAL_GROUP_PRESENCE,
       '--processes', '0']

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)
print('\n\n')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
       '--input', os.path.join(PROJECT_PATH, '01_selected-mol2s'),
       '--id_file', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2ids.txt'),
       '--output', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s'),
       '--whitelist', 'True']


print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)
print('\n\nSELECTED MOL2s:')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
       '--input', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s')]

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)


##############################################################################


s = """

################################################
Step 03: PREFILTER BY FUNCTIONAL GROUP DISTANCE
################################################
"""
print(s)

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'funcgroup_distance_to_id.py'),
       '--input', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s'),
       '--output', os.path.join(PROJECT_PATH, '03_3keto-and-sulfur-13-20A_mol2ids.txt'),
       '--selection', FUNCTIONAL_GROUP_DISTANCE_SELECTION,
       '--distance', FUNCTIONAL_GROUP_DISTANCE,
       '--processes', '0']

subprocess.call(cmd)
print('\n\n')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'id_to_mol2.py'),
       '--input', os.path.join(PROJECT_PATH, '02_3keto-and-sulfur-mol2s'),
       '--id_file', os.path.join(PROJECT_PATH, '03_3keto-and-sulfur-13-20A_mol2ids.txt'),
       '--output', os.path.join(PROJECT_PATH, '03_3keto-and-sulfur-13-20A_mol2s'),
       '--whitelist', 'True']


print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)
print('\n\nSELECTED MOL2s:')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
       '--input', os.path.join(PROJECT_PATH, '03_3keto-and-sulfur-13-20A_mol2s')]

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)


##############################################################################


s = """

################################################
Step 04: OMEGA CONFOMERS
################################################
"""
print(s)


cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'run_omega.py'),
       '--input', os.path.join(PROJECT_PATH, '03_3keto-and-sulfur-13-20A_mol2s'),
       '--output', os.path.join(PROJECT_PATH, '04_omega_confomers'),
       '--executable', OMEGA_EXECUTABLE,
       '--processes', '0']

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)
print('\n\nSELECTED MOL2s:')

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'count_mol2.py'),
       '--input', os.path.join(PROJECT_PATH, '04_omega_confomers')]

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)

s = """

################################################
Step 05: ROCS OVERLAYS
################################################
"""
print(s)

cmd = ['python', os.path.join(SCREENLAMP_TOOLS_DIR, 'run_rocs.py'),
       '--input', os.path.join(PROJECT_PATH, '04_omega_confomers'),
       '--output', os.path.join(PROJECT_PATH, '05_rocs_overlays'),
       '--executable', ROCS_EXECUTABLE,
       '--processes', '0']

print('Running command:\n%s\n' % ' '.join(cmd))
subprocess.call(cmd)
