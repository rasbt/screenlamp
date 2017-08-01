# Tools API


This page serves as a quick lookup reference for the different modules within screenlamp.Please see the Tools Tutorial for a more detailed explanation of the different modules and how they can be combined in a typical virtual screening pipeline.


## count_mol2.py



**Usage:**

     count_mol2.py [-h] -i INPUT [-v]


A command line tool for counting the number of molecules in MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to a `.mol2` or `.mol2.gz`file,
or a directory containing `.mol2`/`.mol2.gz` files
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python count_mol2.py -i mol2_dir/
python count_mol2.py -i partition_1.mol2
```



## datatable_to_id.py



**Usage:**

     datatable_to_id.py [-h] -i INPUT -o OUTPUT --id_column ID_COLUMN


`[--seperator SEPERATOR] [-s SELECTION] [-v VERBOSE]`  
`[--version]`  
Create a text file with molecule IDs from MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to a datatable file where each row
represents a molecule and each columns
store the molecular features
- `-o OUTPUT, --output OUTPUT`  
Output path for the ID file (For example, `ids.txt`)
- `--id_column ID_COLUMN`  
Name of the Molecule ID column
- `--seperator SEPERATOR`  
Column seperator used
in the input table
- `-s SELECTION, --selection SELECTION`  
A conditional selection string:
- Single column selection example: `"(MWT > 500)"`
- Logical OR example: `"(MWT > 500) | (MWT < 200)"`
- Logical AND example: `"(NRB <= 7) & (MWT > 200)"`
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any
output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python datatable_to_id.py\
--input table.txt\
--output ids.txt\
--id_column ZINC_ID\
--selection "(NRB <= 7) & (MWT > 200)"
```



## funcgroup_distance_to_id.py



**Usage:**

     funcgroup_distance_to_id.py [-h] [-i INPUT] [-o OUTPUT] -s SELECTION


`[-v VERBOSE] -d DISTANCE`  
`[--processes PROCESSES] [--version]`  
A command line tool for filtering mol2 files
by the presence of atoms or functional groups.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to a .mol2 or .mol2.gz file,
or a directory containing .mol2/.mol2.gzfiles
- `-o OUTPUT, --output OUTPUT`  
Directory for writing the output files
- `-s SELECTION, --selection SELECTION`  
Selection condition for the atom distance checks.
1) Selection example to compare 2 atom types:
"(atom_type == 'S.o2') --> (atom_type == 'O.2')"
2) Selection example to consider either an S.o2 or S.3 atom to an O.2 atom:
"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"
3) Selection example using logical ORs on both sides:
"((atom_type == 'S.3') | (atom_type == 'S.o2')) -->  ((atom_type == 'O.2') | (atom_type == 'O.3'))"
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any output.
If 1 (default), prints the file currently processing.
- `-d DISTANCE, --distance DISTANCE`  
A distance range formatted
as "lowerbound-upperbound".
For example, if 13-20 is provided as an
argument, two atoms are considered a match
if they are not closer than 13 angstroms and
not farther than 20 angstroms.
- `--processes PROCESSES`  
Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `--version             show program's version number and exit`  
The following example how to select those molecules
that contain S.2 or S.o2 atom that is within
a 13-20 angstroms distance to a O.2 atom:
`python funcgroup_distance_to_id.py\`  
- `--input mol2_dir/\`  
- `--output ids.txt\`  
- `--selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"\`  
- `--distance 13-20\`  
- `--processes 0`  


## funcgroup_matching.py



**Usage:**

     funcgroup_matching.py [-h] -i INPUT -o OUTPUT [-d MAX_DISTANCE]


`[--processes PROCESSES] [-v VERBOSE] [--version]`  
Generates tab-separated tables with containing atom
type and charge information from matching
atoms in pair-wise overlays.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to a directory containing pairs
of *_query.mol2/.mol2.gz
and *_dbase.mol2/.mol2.gz files
- `-o OUTPUT, --output OUTPUT`  
Path to a directory for writing
the output files
- `-d MAX_DISTANCE, --max_distance MAX_DISTANCE`  
The maximum distance, in angstroms, the
overlayed atoms can be apart from each
other for being considered a match.
For instance, a --max_distance 1.3 (default)
would count atoms as a match if they
are within 0 and 1.3 angstroms
to the target atom.
- `--processes PROCESSES`  
Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any output.
If 1 (default), prints the file currently processing.
- `--version             show program's version number and exit`  

**Example:**

```
python funcgroup_matching.py\
--input rocs_overlays_sorted/\
--output matching_tables/\
--max_distance 1.3\
--processes 0
```



## funcgroup_matching_selection.py



**Usage:**

     funcgroup_matching_selection.py [-h] -i INPUT -o OUTPUT


`[--atomtype_selection ATOMTYPE_SELECTION]`  
`[--charge_selection CHARGE_SELECTION]`  
`[--input_mol2 INPUT_MOL2] [-v VERBOSE]`  
`[--version]`  

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input directory with input .tsv files
- `-o OUTPUT, --output OUTPUT`  
Directory for writing the output files
- `--atomtype_selection ATOMTYPE_SELECTION`  
Directory for writing the output files
- `--charge_selection CHARGE_SELECTION`  
Directory for writing the output files
- `--input_mol2 INPUT_MOL2`  
Directory for writing the output files
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any
output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python funcgroup_matching_selection.py\
--input 07_fgroup_matching_tables\
--input_mol2 06_rocs_overlays_sorted\
--output 08_funcgroup_selection\
--atomtype_selection "((S1 == 'S.3') | (S1 == 'S.o2')) --> (O2 == 'O.2')"\
--charge_selection FGROUP_CHARGE "((S1 >= 1.0)) --> (O2 <= -0.5)"
```



## funcgroup_presence_to_id.py



**Usage:**

     funcgroup_presence_to_id.py [-h] [-i INPUT] [-o OUTPUT] -s SELECTION


`[--processes PROCESSES] [-v VERBOSE]`  
`[--version]`  
Selecting molecules base on the presence
of certain atoms or functional groups.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input directory with .mol2 and .mol2.gz files
- `-o OUTPUT, --output OUTPUT`  
Directory for writing the output files
- `-s SELECTION, --selection SELECTION`  
Selection condition for the atom presence checks.
1) Require 2 atom types to be present:
"(atom_type == 'S.o2') --> (atom_type == 'O.2')"
2) Selection example to consider either an S.o2 or S.3 atom and a O.2 atom to be present:
"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"
3) Selection example using logical ORs on both sides:
"((atom_type == 'S.3') | (atom_type == 'S.o2')) -->  ((atom_type == 'O.2') | (atom_type == 'O.3'))"
- `--processes PROCESSES`  
Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any
output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python funcgroup_presence_to_id.py --input mol2s/\
--output mol2ids.txt\
--selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"\
--processes 0
```



## id_to_mol2.py



**Usage:**

     id_to_mol2.py [-h] -i INPUT --id_file ID_FILE -o OUTPUT [-w WHITELIST]


`[-v VERBOSE] [--version]`  
Create filtered MOL2 files from ID and input MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input .mol2 or .mol2.gz file,or a directory of MOL2 files
- `--id_file ID_FILE     Input ID file that contains molecule`  
IDs (one ID per line)
- `-o OUTPUT, --output OUTPUT`  
Output directory path for the
filtered MOL2 files
- `-w WHITELIST, --whitelist WHITELIST`  
Uses ID file as whitelist if True (default).
Uses ID file as blacklist if False.
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any
output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python id_to_mol2.py --input mol2_dir/\
--id_file ids.txt\
--whitelist True\
--output filtered_mol2_dir/
```



## merge_id_files.py



**Usage:**

     merge_id_files.py [-h] --input1 INPUT1 --input2 INPUT2 --output OUTPUT


`[--version]`  
Merges two Molecule ID files into
while preventing duplicate entries.

**Arguments:**


- `-h, --help       show this help message and exit`  
- `--input1 INPUT1  Input ID file that contains molecule`  
IDs (one ID per line)
- `--input2 INPUT2  Input ID file that contains molecule`  
IDs (one ID per line)
- `--output OUTPUT  Path to the output ID file`  
- `--version        show program's version number and exit`  

**Example:**

```
python merge_id_files.py\
--input1 mol2s_1.txt\
--input2 mol2s_2.txt\
--output merged.txt
```



## mol2_to_id.py



**Usage:**

     mol2_to_id.py [-h] -i INPUT -o OUTPUT [-v VERBOSE] [--version]


Write a file with molecule IDs from MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input .mol2 or .mol2.gz file,or a directory of MOL2 files
- `-o OUTPUT, --output OUTPUT`  
Output path for the ID file. For example, ids.txt
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.
- `--version             show program's version number and exit`  

**Example:**

```
python mol2_to_id.py\
--input mol2_dir\
--output ids.txt
```



## run_omega.py



**Usage:**

     run_omega.py [-h] -i INPUT -o OUTPUT [--executable EXECUTABLE]


`[--settings SETTINGS] [-p PROCESSES] [-v]`  
Wrapper running OpenEye OMEGA on one
or more database partitions.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input directory with .mol2 and .mol2.gz files
- `-o OUTPUT, --output OUTPUT`  
Directory for writing the output files
- `--executable EXECUTABLE`  
OMEGA2 executable
- `--settings SETTINGS   OMEGA2 settings to use`  
- `-p PROCESSES, --processes PROCESSES`  
Number of processes to run in parallel.
Uses all CPUs if 0
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python run_omega.py\
--input dbase_mol2\
--output dbase_conformers/\
--executable /.../omega2-2.5.1.4\
--processes 0
```



## run_rocs.py



**Usage:**

     run_rocs.py [-h] -i INPUT -o OUTPUT --query QUERY


`[--executable EXECUTABLE] [--settings SETTINGS]`  
`[-p PROCESSES] [-v]`  
Wrapper running OpenEye ROCS on one
or more database partitions.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to input directory containing the database
molecules in .mol2 and/or .mol2.gz format
.mol2.gz data
- `-o OUTPUT, --output OUTPUT`  
Directory path for writing the .mol2 overlay
ROCS status and ROCS report (.rpt) files
- `--query QUERY         Path to the query molecule`  
in .mol2 and/or .mol2.gz format.
The query molecule file could be a single
structure of multiple-conformers of the same
structure. If a multi-conformer file is
submitted, please make sure that all
conformers in the mol2 file have the same
molecule ID/Name.
- `--executable EXECUTABLE`  
Path to the ROCS executable on this machine
- `--settings SETTINGS   ROCS settings to use`  
- `-p PROCESSES, --processes PROCESSES`  
Number of processes to run in parallel.
Uses all CPUs if 0
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python run_rocs.py\
--input database_conformers/\
--output rocs_overlays/\
--executable /.../rocs-3.2.1.4\
--query query.mol2\
--settings "-rankby TanimotoCombo -maxhits 0 -besthits 0 -progress percent --processes 0"
```



## sort_rocs_mol2.py



**Usage:**

     sort_rocs_mol2.py [-h] -i INPUT -o OUTPUT --query QUERY [-s SORTBY]


`[--selection SELECTION]`  
`[--column_seperator COLUMN_SEPERATOR]`  
`[--id_suffix ID_SUFFIX] [-v VERBOSE] [--version]`  
Sorts ROCS results by score and creates
separate .mol2 files for the database and query molecules.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input directory with results from a ROCS run.
- `-o OUTPUT, --output OUTPUT`  
Directory path for writing the .mol2 overlay
ROCS status and ROCS report (.rpt) files
- `--query QUERY         Path to the query molecule`  
in .mol2 and/or .mol2.gz format.
The query molecule file could be a single
structure of multiple-conformers of the same
structure. If a multi-conformer file is
submitted, please make sure that all
conformers in the mol2 file have the same
molecule ID/Name.
- `-s SORTBY, --sortby SORTBY`  
Score column(s) in ROCS report files that
the structures should be sorted by
- `--selection SELECTION`  
Selection string to exclude molecules above
or below a certain score threshold
- `--column_seperator COLUMN_SEPERATOR`  
Column separator used in the ROCS report files
- `--id_suffix ID_SUFFIX`  
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python sort_rocs_mol2.py -i rocs_results/\
--output rocs_sorted/ --query mol.mol2\
--sortby TanimotoCombo,ColorTanimoto\
--selection "(TanimotoCombo >= 0.75) & (ColorTanimoto >= 0.1)"
```

