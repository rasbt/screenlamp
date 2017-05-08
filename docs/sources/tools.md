

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
