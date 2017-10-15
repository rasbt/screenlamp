# Tools


This page serves as a quick lookup reference for the different modules within screenlamp. Please see the [Toolkit Tutorial](tools-tutorial-1) for a more detailed explanation of the different modules and how they can be combined in a typical virtual screening pipeline.


## generate_conformers_omega.py



**Usage:**

     generate_conformers_omega.py [-h] -i INPUT -o OUTPUT --executable


EXECUTABLE [--settings SETTINGS]
`[--processes PROCESSES] [-v]`  
Wrapper running OpenEye OMEGA on one
or more database partitions.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input directory with `.mol2` and `.mol2.gz` files.
- `-o OUTPUT, --output OUTPUT`  
Directory for writing the output files.
- `--executable EXECUTABLE`  
(Required.) The path or command for running
OpenEye OMEGA2 on your system.
- `--settings SETTINGS   (Optional.) OMEGA settings to use.`  
- `--processes PROCESSES`  
(Optional, default: `1`.) Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python generate_conformers_omega.py\
--input dbase_mol2\
--output dbase_conformers/\
--executable /.../omega2-2.5.1.4\
--processes 0
```



## generate_conformers_obabel.py



**Usage:**

     generate_conformers_obabel.py [-h] -i INPUT -o OUTPUT --executable


EXECUTABLE [--settings SETTINGS] [-v]
Wrapper running OpenBabel Confab on one
or more database partitions. Please see
http://open-babel.readthedocs.io/en/latest/3DStructureGen/multipleconformers.html
if you want to learn more about OpenBabel Confab.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Input directory with `.mol2` and `.mol2.gz` files.
- `-o OUTPUT, --output OUTPUT`  
Directory for writing the output files.
- `--executable EXECUTABLE`  
(Required.) The path or command for running
OpenBabel Confab on your system.
- `--settings SETTINGS   (Optional.) OpenBabel settings to use.`  
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python generate_conformers_obabel.py\
--input dbase_mol2/\
--output dbase_conformers/\
--executable /.../obabel
```



## merge_id_files.py



**Usage:**

     merge_id_files.py [-h] -i1 INPUT1 -i2 INPUT2 -o OUTPUT [--version]


Merges two Molecule ID files
(e.g., created via `datatable_to_id.py`, `funcgroup_presence_to_id.py`
or `mol2_to_id.py`) into a single ID file
while preventing duplicate entries.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i1 INPUT1, --input1 INPUT1`  
(Required.) Input ID file that contains molecule
IDs (one ID per line).
- `-i2 INPUT2, --input2 INPUT2`  
(Required.) Input ID file that contains molecule
IDs (one ID per line).
- `-o OUTPUT, --output OUTPUT`  
(Required.) Path to the output ID file.
- `--version             show program's version number and exit`  

**Example:**

```
python merge_id_files.py\
--input1 mol2s_1.txt\
--input2 mol2s_2.txt\
--output merged.txt
```



## overlay_molecules_shapeit.py



**Usage:**

     overlay_molecules_shapeit.py [-h] -i INPUT -o OUTPUT --query QUERY


--executable EXECUTABLE
`[--settings SETTINGS] [-v]`  
Wrapper running Silicos-it Shape-it on one
or more database partitions.
For more information about Shape-it, please see http://silicos-it.be.s3-website-eu-west-1.amazonaws.com/software/shape-it/1.0.1/shape-it.html

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to input directory containing the database
molecules in `.mol2` and/or `.mol2.gz` format.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory path for writing the `.mol2`
overlays and Shape-it score/report (`.rpt`) files.
- `--query QUERY         (Required.) Path to the query molecule`  
in `.mol2` and/or `.mol2.gz` format.
The query molecule file could be a single
structure of multiple-conformers of the same
structure. If a multi-conformer file is
submitted, please make sure that all
conformers in the mol2 file have the same
molecule ID/Name.
- `--executable EXECUTABLE`  
(Required.) The path or command for running
Slicos-it Shape-it on your system.
- `--settings SETTINGS   (Optional, default:" --rankBy Tanimoto")`  
shape-it settings to use.
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python overlay_molecules_shapeit.py\
--input database_conformers/\
--output shapeit_overlays/\
--executable 'shape-it'\
--query query.mol2\
--settings "--rankby Tanimoto
```



## overlay_molecules_rocs.py



**Usage:**

     overlay_molecules_rocs.py [-h] -i INPUT -o OUTPUT --query QUERY


--executable EXECUTABLE [--settings SETTINGS]
`[--processes PROCESSES] [-v]`  
Wrapper running OpenEye ROCS on one
or more database partitions.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
Path to input directory containing the database
molecules in `.mol2` and/or `.mol2.gz` format.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory path for writing the `.mol2`
overlay ROCS status and ROCS report (`.rpt`) files.
- `--query QUERY         (Required.) Path to the query molecule`  
in `.mol2` and/or `.mol2.gz` format.
The query molecule file could be a single
structure of multiple-conformers of the same
structure. If a multi-conformer file is
submitted, please make sure that all
conformers in the mol2 file have the same
molecule ID/Name.
- `--executable EXECUTABLE`  
(Required.) The path or command for running
OpenEye ROCS on your system.
- `--settings SETTINGS   (Optional, default:" -rankby TanimotoCombo -maxhits 0 -besthits 0 -progress percent")`  
ROCS settings to use.
- `--processes PROCESSES`  
(Optional, default: `1`.) Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python overlay_molecules_rocs.py\
--input database_conformers/\
--output rocs_overlays/\
--executable /.../rocs-3.2.1.4\
--query query.mol2\
--settings "-rankby TanimotoCombo -maxhits 0 -besthits 0 -progress percent"\
--processes 0
```



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
(Required.) Path to a directory containing pairs
of `*_query.mol2`/`.mol2.gz`
and `*_dbase.mol2`/`.mol2.gz` files
- `-o OUTPUT, --output OUTPUT`  
(Required.) Path to a directory for writing
the output files
- `-d MAX_DISTANCE, --max_distance MAX_DISTANCE`  
(Optional, default: `1.3`.) The maximum distance,
in angstroms, the
overlayed atoms can be apart from each
other for being considered a match.
For instance, a --max_distance 1.3 (default)
would count atoms as a match if they
are within 0 and 1.3 angstroms
to the target atom.
- `--processes PROCESSES`  
(Optional, default: `1`.) Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any output.
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



## sort_rocs_mol2.py



**Usage:**

     sort_rocs_mol2.py [-h] -i INPUT -o OUTPUT --query QUERY [-s SORTBY]


`[--selection SELECTION] [--separator SEPARATOR]`  
`[--id_suffix ID_SUFFIX] [-v VERBOSE] [--version]`  
Sorts ROCS results by score and creates
separate .mol2 files for the database and query molecules.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Input directory with results from a ROCS run.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory path for writing the `.mol2` overlay
ROCS status and ROCS report (`.rpt`) files
- `--query QUERY         (Required.) Path to the query molecule`  
in `.mol2` and/or `.mol2.gz` format.
The query molecule file could be a single
structure of multiple-conformers of the same
structure. If a multi-conformer file is
submitted, please make sure that all
conformers in the mol2 file have the same
molecule ID/Name.
- `-s SORTBY, --sortby SORTBY`  
(Optional, default: `"TanimotoCombo,ColorTanimoto"`)
Score column(s) in ROCS report files that
the structures should be sorted by.
- `--selection SELECTION`  
(Optional, default: `"(TanimotoCombo >= 1.0)) & (ColorTanimoto >= 0.25)"`)
Selection string to exclude molecules above
or below a certain score threshold. By default
all molecules with a ColorTanimoto score smaller than 0.25
and a TanimotoCombo score smaller than 1.0 will be disregarded.
- `--separator SEPARATOR`  
(Optional, default: `"\t"`.) Column separator used
in the input table.
Assumes tab-separated values by default.
- `--id_suffix ID_SUFFIX`  
(Optional, default: `"False"`.)
If `--id_suffix "True"`, a molecule ID suffix
will be added to the query
molecules in the order the ROCS query molecules
appear in a multi-conformer query file.
For instance, if all query molecules are labeled "3kPZS",
then the same structures in the output file are labeled
3kPZS_1, 3kPZS_2, ... Note that those modified conformer
will correspond to the conformer names in the ROCS report
tables. However, they may appear in an unsorted order in
the _query files, which are sorted by the overlay score
of the database molecules. For example, if the
database molecule is called ZINC123_112, first
entry in the _query file that corresponds to *_dbase
file may by labeled 3kPZS_11 if the 11th 3kPZS conformer
is the best match according to ROCS.
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



## count_mol2.py



**Usage:**

     count_mol2.py [-h] -i INPUT [-v]


A command line tool for counting the number of molecules in MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Path to a `.mol2` or `.mol2.gz`file,
or a directory containing `.mol2`/`.mol2.gz` files.
- `-v, --version`  
Show program's version number and exit

**Example:**

```
python count_mol2.py -i mol2_dir/
python count_mol2.py -i partition_1.mol2
```



## funcgroup_matching_selection.py



**Usage:**

     funcgroup_matching_selection.py [-h] -i INPUT [--input_mol2 INPUT_MOL2]


-o OUTPUT
`[--atomtype_selection ATOMTYPE_SELECTION]`  
`[--charge_selection CHARGE_SELECTION]`  
`[-v VERBOSE] [--version]`  
Selects molecules with certain functional group matching patterns after functional group matching.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Input directory with input `.tsv` tables (functional group files generated via `funcgroup_matching.py`).
- `--input_mol2 INPUT_MOL2`  
(Optional.) Input directory with input `.mol2` structures (ROCS overlays
generated via `sort_rocs_mol2.py`). If provided, the MOL2 structures
corresponding to the selected matches will be extracted from the
input_mol2 directory and written to the output directory for visual inspection,
for example, using PyMOL.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory for writing the output files.
- `--atomtype_selection ATOMTYPE_SELECTION`  
(Optional, default="") Selection condition for the atom types.
For example, the following selection query will make a selection based on
matching 2 atoms in the reference molecule, S1 and O2:
"((S1 == 'S.3') | (S1 == 'S.o2')) --> (O2 == 'O.2')".
Here, S1 can either match an S.3 or an S.o2 atom in the database molecule.
The second atom, O2, must match an atom of type O.2.
- `--charge_selection CHARGE_SELECTION`  
(Optional, default="") Selection condition for the atom charges.
For example, the following selection query will make a selection based on
matching the charges in 2 atoms in the reference molecule, S1 and O2:
"((S1 >= 1.0)) --> (O2 <= -0.5)".
Here, the atom that matches S1 has to have a positive charge, 1 or greater. The charge
matching the second atom, O2, must be (partially) negative (-0.5 or smaller).
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any
output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python funcgroup_matching_selection.py\
--input 07_fgroup_matching_tables # generated via funcgroup_matching.py\
--input_mol2 06_rocs_overlays_sorted # generated via sort_rocs_mol2.py\
--output 08_funcgroup_selection\
--atomtype_selection "((S1 == 'S.3') | (S1 == 'S.o2')) --> (O2 == 'O.2')"\
--charge_selection FGROUP_CHARGE "((S1 >= 1.0)) --> (O2 <= -0.5)"
```



## enumerate_conformers.py



**Usage:**

     enumerate_conformers.py [-h] -i INPUT -o OUTPUT [-v VERBOSE]


`[--version]`  
Numbers molecules in MOL2 files by adding a suffix as index. For example, if there are three molecules in a MOL2 file, moleculeabc_0, moleculeabc_1, and moleculedef_0,
those molecules will be relabeled to moleculeabc_0, moleculeabc_1, and moleculedef_0.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Path to a `.mol2` or `.mol2.gz`file,
or a directory containing `.mol2`/`.mol2.gz` files.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory path for writing the numbered MOL2s
- `-v VERBOSE, --verbose VERBOSE`  
Verbosity level. If 0, does not print any output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python enumerate_conformers.py -i conformer_mol2s/\
--output numbered_conformers/
```



## id_to_mol2.py



**Usage:**

     id_to_mol2.py [-h] -i INPUT --id_file ID_FILE -o OUTPUT


`[-w INCLUDELIST] [-v VERBOSE] [--version]`  
Create filtered MOL2 files from ID and input MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Input `.mol2` or `.mol2.gz` file, or a directory of MOL2 files.
- `--id_file ID_FILE     (Required.) Input ID file that contains molecule`  
IDs (one ID per line).
- `-o OUTPUT, --output OUTPUT`  
(Required.) Output directory path for the
filtered MOL2 files.
- `-w INCLUDELIST, --includelist INCLUDELIST`  
(Optional, default: `True`.) Uses ID file as includelist if True (default).
Uses ID file as excludelist if False.
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any
output.
If 1 (default), prints the file currently
processing.
- `--version             show program's version number and exit`  

**Example:**

```
python id_to_mol2.py --input mol2_dir/\
--id_file ids.txt\
--includelist True\
--output filtered_mol2_dir/
```



## funcgroup_distance_to_id.py



**Usage:**

     funcgroup_distance_to_id.py [-h] -i INPUT -o OUTPUT -s SELECTION -d


DISTANCE [--processes PROCESSES]
`[-v VERBOSE] [--version]`  
A command line tool for filtering mol2 files
by the distance of two atoms or functional groups.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Path to a `.mol2` or `.mol2.gz` file,
or a directory containing `.mol2`/`.mol2.gz`files.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory for writing the output files.
- `-s SELECTION, --selection SELECTION`  
(Required.) Selection condition for the atom distance checks.
1) Selection example to compare 2 atom types:
`"(atom_type == 'S.o2') --> (atom_type == 'O.2')"`.
2) Selection example to consider either an S.o2 or S.3 atom to an O.2 atom:
`"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"`.
3) Selection example using logical ORs on both sides:
`"((atom_type == 'S.3') | (atom_type == 'S.o2')) -->  ((atom_type == 'O.2') | (atom_type == 'O.3'))"`.
- `-d DISTANCE, --distance DISTANCE`  
(Required.) A distance range formatted
as "lowerbound-upperbound".
For example, if 13-20 is provided as an
argument, two atoms are considered a match
if they are not closer than 13 angstroms and
not farther than 20 angstroms.
- `--processes PROCESSES`  
(Optional, default: `1`.) Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any output.
If 1 (default), prints the file currently processing.
- `--version             show program's version number and exit`  

**Example:**

```
python funcgroup_distance_to_id.py\
--input mol2_dir/\
--output ids.txt\
--selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"\
--distance 13-20\
--processes 0
\# The example above selects those molecules
\# that contain S.2 or S.o2 atom that is within
\# a 13-20 angstroms distance to an 'O.2' (sp2/keto oxygen) atom
```



## mol2_to_id.py



**Usage:**

     mol2_to_id.py [-h] -i INPUT -o OUTPUT [-v VERBOSE] [--version]


Writes a file with molecule IDs from MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Input `.mol2` or `.mol2.gz` file,or a directory of MOL2 files.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Output path for the ID file. For example, `ids.txt`.
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.
- `--version             show program's version number and exit`  

**Example:**

```
python mol2_to_id.py\
--input mol2_dir\
--output ids.txt
```



## datatable_to_id.py



**Usage:**

     datatable_to_id.py [-h] -i INPUT -o OUTPUT --id_column ID_COLUMN


`[--separator SEPARATOR] [-s SELECTION] [-v VERBOSE]`  
`[--version]`  
Create a text file with molecule IDs from MOL2 files.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Path to a datatable file where each
row represents a molecule and each columns
store the molecular features.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Output path for the ID file (for example, `ids.txt`).
- `--id_column ID_COLUMN`  
(Required.) Name of the Molecule ID column.
- `--separator SEPARATOR`  
(Optional, default: `"	"`.) Column separator used
in the input table.
Assumes tab-separated values by default.
- `-s SELECTION, --selection SELECTION`  
(Optional, default: `None`.) A conditional selection string:
Single column selection example: `"(MWT > 500)"`.  Logical OR example: `"(MWT > 500) | (MWT < 200)"`. Logical AND example: `"(NRB <= 7) & (MWT > 200)"`.
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any
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



## funcgroup_presence_to_id.py



**Usage:**

     funcgroup_presence_to_id.py [-h] -i INPUT -o OUTPUT -s SELECTION


`[--processes PROCESSES] [-v VERBOSE]`  
`[--version]`  
Checking molecules base on the presence
of certain atoms or functional groups and writing the results to a text file.

**Arguments:**


- `-h, --help`  
Show this help message and exit
- `-i INPUT, --input INPUT`  
(Required.) Input directory with `.mol2` and `.mol2.gz` files.
- `-o OUTPUT, --output OUTPUT`  
(Required.) Directory for writing the output files.
- `-s SELECTION, --selection SELECTION`  
Selection condition for the atom presence checks.
1) Require 2 atom types to be present:
"(atom_type == 'S.o2') --> (atom_type == 'O.2')"
2) Selection example to consider either an S.o2 or S.3 atom and a O.2 atom to be present:
"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"
3) Selection example using logical ORs on both sides:
"((atom_type == 'S.3') | (atom_type == 'S.o2')) -->  ((atom_type == 'O.2') | (atom_type == 'O.3'))"
- `--processes PROCESSES`  
(Optional, default: `1`.) Number of processes to run in parallel.
If processes > 0, the specified number of CPUs
will be used.
If processes = 0, all available CPUs will
be used.
If processes = -1, all available CPUs
minus `processes` will be used.
- `-v VERBOSE, --verbose VERBOSE`  
(Optional, default: `1`.) Verbosity level. If 0, does not print any
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

