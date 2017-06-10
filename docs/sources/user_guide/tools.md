

# count_mol2.py



**Usage:**

    count_mol2.py [-h] [-i INPUT] [-v]


A command line tool for counting MOL2 structures


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input .mol2 or .mol2.gz file,or a directory of MOL2 files

- `-v, --version         show program's version number and exit`

**Example:**

```
python count_mol2.py -i mol2_dir
```


# datatable_to_id.py



**Usage:**

    datatable_to_id.py [-h] -i INPUT -o OUTPUT --id_column ID_COLUMN


    - [--seperator SEPERATOR] -s SELECTION [-v VERBOSE]

    - [--version]

Write a file with molecule IDs from MOL2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input .mol2 or .mol2.gz file,or a directory of MOL2 files

- `-o OUTPUT, --output OUTPUT`
    - Output path for the ID file. For example, ids.txt

- `--id_column ID_COLUMN`
    - ID column.

- `--seperator SEPERATOR`
    - Column seperator

- `-s SELECTION, --selection SELECTION`
    - Selection string For example, ...

- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `--version             show program's version number and exit`

**Example:**

```
python mol2_to_id.py -i mol2_dir -o ids.txt
```


# funcgroup_distance_to_id.py



**Usage:**

    funcgroup_distance_to_id.py [-h] [-i INPUT] [-o OUTPUT] -s SELECTION


    - [-v VERBOSE] [-d DISTANCE]

    - [--processes PROCESSES] [--version]

A command line tool for filtering mol2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input directory with .mol2 and .mol2.gz files

- `-o OUTPUT, --output OUTPUT`
    - Directory for writing the output files

- `-s SELECTION, --selection SELECTION`
    - Selection string For example, ...

- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `-d DISTANCE, --distance DISTANCE`
    - Distance as "lowerbound-upperbound"

- `--processes PROCESSES`
    - Number of processes to run in parallel. If processes>0, the specified number of CPUs will be used. If processes=0, all available CPUs will be used. If processes=-1, all available CPUs minus `processes` will be used.

- `--version             show program's version number and exit`


# funcgroup_matching.py



**Usage:**

    funcgroup_matching.py [-h] -i INPUT -o OUTPUT [-v VERBOSE] [--version]


A command line tool for filtering mol2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input directory with .mol2 and .mol2.gz files

- `-o OUTPUT, --output OUTPUT`
    - Directory for writing the output files

- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `--version             show program's version number and exit`


# funcgroup_to_id.py



**Usage:**

    funcgroup_to_id.py [-h] [-i INPUT] [-o OUTPUT] -s SELECTION


    - [-v VERBOSE] [--processes PROCESSES] [--version]

A command line tool for filtering mol2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input directory with .mol2 and .mol2.gz files

- `-o OUTPUT, --output OUTPUT`
    - Directory for writing the output files

- `-s SELECTION, --selection SELECTION`
    - Selection string For example, ...

- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `--processes PROCESSES`
    - Number of processes to run in parallel. If processes>0, the specified number of CPUs will be used. If processes=0, all available CPUs will be used. If processes=-1, all available CPUs minus `processes` will be used.

- `--version             show program's version number and exit`


# id_to_mol2.py



**Usage:**

    id_to_mol2.py [-h] -i INPUT --id_file ID_FILE -o OUTPUT [-w WHITELIST]


    - [-v VERBOSE] [--version]

Write a file with molecule IDs from MOL2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input .mol2 or .mol2.gz file,or a directory of MOL2 files

- `--id_file ID_FILE     Input ID file that contains moleculeIDs (one ID per line)`
- `-o OUTPUT, --output OUTPUT`
    - Output directory path for the filtered MOL2 files

- `-w WHITELIST, --whitelist WHITELIST`
    - Uses ID file as whitelist if True (default). Uses ID file as blacklist if False.

- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `--version             show program's version number and exit`

**Example:**

```
python mol2_to_id.py -i mol2_dir -o ids.txt
```


# mol2_to_id.py



**Usage:**

    mol2_to_id.py [-h] -i INPUT -o OUTPUT [-v VERBOSE] [--version]


Write a file with molecule IDs from MOL2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input .mol2 or .mol2.gz file,or a directory of MOL2 files

- `-o OUTPUT, --output OUTPUT`
    - Output path for the ID file. For example, ids.txt

- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `--version             show program's version number and exit`

**Example:**

```
python mol2_to_id.py -i mol2_dir -o ids.txt
```


# run_omega.py



**Usage:**

    run_omega.py [-h] -i INPUT -o OUTPUT [--executable EXECUTABLE]


    - [--settings SETTINGS] [-p PROCESSES] [-v]

A command line tool for filtering mol2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input directory with .mol2 and .mol2.gz files

- `-o OUTPUT, --output OUTPUT`
    - Directory for writing the output files

- `--executable EXECUTABLE`
    - OMEGA2 executable

- `--settings SETTINGS   Additional OMEGA2 settings`
- `-p PROCESSES, --processes PROCESSES`
    - Number of processes to run in parallel. Uses all CPUs if 0

- `-v, --version         show program's version number and exit`


# run_rocs.py



**Usage:**

    run_rocs.py [-h] -i INPUT -o OUTPUT [--query QUERY]


    - [--executable EXECUTABLE] [--settings SETTINGS]

    - [-p PROCESSES] [-v]

A command line tool for filtering mol2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input directory with .mol2 and .mol2.gz files

- `-o OUTPUT, --output OUTPUT`
    - Directory for writing the output files

- `--query QUERY         Query molecule`
- `--executable EXECUTABLE`
    - ROCS executable

- `--settings SETTINGS   Additional ROCS settings`
- `-p PROCESSES, --processes PROCESSES`
    - Number of processes to run in parallel. Uses all CPUs if 0

- `-v, --version         show program's version number and exit`


# sort_rocs_mol2.py



**Usage:**

    sort_rocs_mol2.py [-h] -i INPUT -o OUTPUT -q QUERY [-s SORTBY]


    - [--column_seperator COLUMN_SEPERATOR] [-v VERBOSE]

    - [--version]

A command line tool for filtering mol2 files.


**Optional Arguments:**


- `-h, --help            show this help message and exit`
- `-i INPUT, --input INPUT`
    - Input directory with .mol2 and .mol2.gz files

- `-o OUTPUT, --output OUTPUT`
    - Directory for writing the output files

- `-q QUERY, --query QUERY`
    - Query molecule file

- `-s SORTBY, --sortby SORTBY`
- `--column_seperator COLUMN_SEPERATOR`
- `-v VERBOSE, --verbose VERBOSE`
    - Verbosity level. If 0, does not print any output. If 1 (default), prints the file currently processing.

- `--version             show program's version number and exit`
