

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
