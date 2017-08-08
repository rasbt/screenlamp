# Screenlamp Toolkit Tutorial

This tutorial explains how the individual screenlamp tools (located in the `screenlamp/tools` subdirectory) work in the context of a small virtual screening example. 

The dataset and workflow we are going to use is simililar to the [Pipeline Tutorial](pipeline-tutorial-1/index.html), which uses a preconstructed, automated virtual pipeline based using the tools explained in this tutorial. While the [Pipeline Tutorial](pipeline-tutorial-1/index.html) provides a high level overview and a more convenient, preconstructred pipeline, this tool aims to explain the building blocks behind it so that users can understand and learn how to construct their own pipelines and/or modify the existing pipeline presented in the [Pipeline Tutorial](pipeline-tutorial-1/index.html).

To explain the main steps in a typical filtering pipeline using screenlamp, this tutorial will work through the following individual steps performed by the pipeline in the [Pipeline Tutorial](pipeline-tutorial-1/index.html) incrementally:

![](images/tools-tutorial-1/pipeline-overview.jpg)

## Obtaining and Preparing the Dataset


### MOL2 Input Files

The tools presented in this tutorial can work with MOL2 files of arbitrary size. However, to minimize the computation time for the purposes of illustration, we are only going to use a small subset of molecules.

A typical use case for these would be the screening of all ~18,000,000 *Drug-Like* molecules from [ZINC](http://zinc.docking.org), which is available in MOL2 format on ZINC [here](http://zinc.docking.org/subsets/drug-like). Please note that screenlamp supports both Tripos MOL2 (`*.mol2`) files and gzipped Tripos MOL2 files (`*.mol2.gz`) out of the box. Thus, if your input dataset is in gzipped format, you can use it right away without having to make any adjustments or decompressing it. However, please not that the decompressing and compressing operations that are performed when working with gzipped files have an additional toll on computational performance.

With kind permission from John Irwin and the ZINC team, we are using a random subset of 70,000 small molecules that we prepared for this tutorial. This subset from ZINC is split into 7 multi-MOL2 file with 10,000 molecules each: `partition_mol2_1.mol2` to `partition_mol2_7.mol2`. 

For this tutorial, please download the dataset by clicking the following link and unzip it on your machine that you are using for the virtual screening run: [https://s3-us-west-2.amazonaws.com/screenlamp-datasets/pipeline-tutorial_1/partition_1-7.zip](https://s3-us-west-2.amazonaws.com/screenlamp-datasets/pipeline-tutorial_1/partition_1-7.zip)


### Datatable for Prefiltering

For this particular tutorial you'll also need a datatable containing general information about these molecules. Although the partitions you downloaded above are only a small, modified subset of [ZINC](http://zinc.docking.org) molecules, we are going to use the full ~18,000,000 molecule Drug-like table available for download at [http://zinc.docking.org/subsets/drug-like](http://zinc.docking.org/subsets/drug-like). To download the tab-separated table, click on the [Properties](http://zinc.docking.org/db/bysubset/3/3_prop.xls) link on the [ZINC Drug-like](http://zinc.docking.org/subsets/drug-like) page. Please note that the size of the datatable is about ~1.8 Gb, and thus, the download may take a while depending on your internet connection. Alternatively, we recommend using a smaller datatable containing only ~170,000 molecules; to download this table, please use the following link: [https://s3-us-west-2.amazonaws.com/screenlamp-datasets/pipeline-tutorial_1/small_table_p1-7.txt](https://s3-us-west-2.amazonaws.com/screenlamp-datasets/pipeline-tutorial_1/small_table_p1-7.txt)


### Query Molecule

The third datafile you'll need for ligand-based virtual screening is the query molecule. For this tutorial, please download the following multi-conformer MOL2 file: [https://s3-us-west-2.amazonaws.com/screenlamp-datasets/pipeline-tutorial_1/3kpzs_query.mol2](https://s3-us-west-2.amazonaws.com/screenlamp-datasets/pipeline-tutorial_1/3kpzs_query.mol2)

## Data storage and project layout

After downloading the files described in the previous subsection, create a new directory called `tk-tutorial_data` to store these files. The contents of this `tk-tutorial_data` directory should be as follows:

![](../images/toolkit-tutorial/dataset-overview.png)

Next, we are going to create a new directory, `tutorial-results`, to store the results we are going to generate in this tutorial. Note that throughout this tutorial, the `!` command denotes a new command line terminal prompt (e.g., bash shell):


```python
! mkdir tutorial-results
```

    mkdir: tutorial-results: File exists


---

**Important Note**

All code in this tutorial is executed using a Python 3.6 interpreter. The code has not been tested in Python 2.7.

---

Note that this tutorial assumes that the screenlamp tools are available from a directory `'tools'`, but you can store them wherever you want.

Before we start exploring the tools contained in screenlamp's `tools` folder, let's start with a simple script that we are going to use throughout this tutorial to count the number of structures in a mol2 file or directory containing mol2 files: 

Using the `count_mol2.py` script, we can now count the number of structures in each mol2 file in our input directory like so:


```python
! python tools/count_mol2.py -i tk-tutorial_data/partition_1-7/
```

    partition_1.mol2 : 10000
    partition_2.mol2 : 10000
    partition_3.mol2 : 10000
    partition_4.mol2 : 10000
    partition_5.mol2 : 10000
    partition_6.mol2 : 10000
    partition_7.mol2 : 10000
    Total : 70000


As we can see, each of the 7 partitions in our dataset contains 10,000 molecules, that is, 70,000 structures in total.

## General Blacklist & Whitelist filtering

### Generating ID files from molecules

First, we are going to generate an ID file of all structures in the mol2 files of the 7 partitions. In the context of this tutorial, an "ID file" is a plaintext file that contains the molecule identifiers fetched from the mol2 files. 

We can create such an ID file using the `mol2_to_id.py` script as shown below:


```python
! python tools/mol2_to_id.py \
  --input tk-tutorial_data/partition_1-7/ \
  --output tutorial-results/all-mol2ids.txt
```

    Processing partition_1.mol2 | scanned 10000 molecules | 16925 mol/sec
    Processing partition_2.mol2 | scanned 10000 molecules | 11431 mol/sec
    Processing partition_3.mol2 | scanned 10000 molecules | 9346 mol/sec
    Processing partition_4.mol2 | scanned 10000 molecules | 11809 mol/sec
    Processing partition_5.mol2 | scanned 10000 molecules | 18886 mol/sec
    Processing partition_6.mol2 | scanned 10000 molecules | 18984 mol/sec
    Processing partition_7.mol2 | scanned 10000 molecules | 18110 mol/sec


To check that the creation of the ID file was successful and to see how it generally looks like, we will use the Unix/Linux `head` command line tool to display the first 10 rows of the newly created ID file:


```python
! head tutorial-results/all-mol2ids.txt
```

    ZINC57271411
    ZINC50764925
    ZINC65255333
    ZINC06394508
    ZINC65292537
    ZINC65375610
    ZINC31820077
    ZINC65395084
    ZINC00205726
    ZINC01458151


To illustrate the concept of whitelist and blacklist filtering in the following sections, let us now create a small ID list file, we name it `5-mol2ids.txt`, that contains 5 IDs only:


```python
! echo "\
ZINC65255333\n\
ZINC06394508\n\
ZINC65292537\n\
ZINC65375610\n\
ZINC31820077" > tutorial-results/5-mol2ids.txt
```

### Whitelist Filtering

Now, using the script `id_to_mol2.py`, we can filter a directory of mol2 files for molecules that are listed in a ID file using the `whitefilter True` option. Executing the following command will look for the structures corresponding to the 5 molecule IDs listed in the `5-mol2ids.txt` that we created in the previous section, and write the corresponding structure files to a new directory that we will call `whitelist_example`:


```python
! python tools/id_to_mol2.py \
  --input tk-tutorial_data/partition_1-7/ \
  --output tutorial-results/whitelist-example \
  --id_file tutorial-results/5-mol2ids.txt \
  --whitelist True
```

    Processing partition_1.mol2 | scanned 10000 molecules | 15319 mol/sec
    Processing partition_2.mol2 | scanned 10000 molecules | 14400 mol/sec
    Processing partition_3.mol2 | scanned 10000 molecules | 14980 mol/sec
    Processing partition_4.mol2 | scanned 10000 molecules | 14893 mol/sec
    Processing partition_5.mol2 | scanned 10000 molecules | 14170 mol/sec
    Processing partition_6.mol2 | scanned 10000 molecules | 12873 mol/sec
    Processing partition_7.mol2 | scanned 10000 molecules | 12457 mol/sec
    Finished


The output directory, `tutorial-results/whitelist-example, should now contain only mol2 structures that are labeled with IDs contained in the `5-mol2ids.txt` text file.

Please note that id_to_mol2 creates a new file for each mol2 file it scanned; however, the creation of such a file does not imply that structures were found via whitelist filtering. For example, the 5 structure IDs in the `5-mol2ids.txt` all refer to structures from `partition_1` as we can check by running the already familiar `count_mol2.py` script:


```python
! ls tutorial-results/whitelist-example
```

    partition_1.mol2 partition_3.mol2 partition_5.mol2 partition_7.mol2
    partition_2.mol2 partition_4.mol2 partition_6.mol2



```python
! python tools/count_mol2.py \
  --input tutorial-results/whitelist-example
```

    partition_1.mol2 : 5
    partition_2.mol2 : 0
    partition_3.mol2 : 0
    partition_4.mol2 : 0
    partition_5.mol2 : 0
    partition_6.mol2 : 0
    partition_7.mol2 : 0
    Total : 5


### Blacklist Filtering

Similar to the previous approach, using a whitelist filter, we can do blacklist filtering, which means that all molecules are selected ***but*** the ones contained in an ID file. In order to perform blacklist filtering, we use the setting `--whitelist False` as shown below:


```python
! python tools/id_to_mol2.py \
  --input tk-tutorial_data/partition_1-7/ \
  --output tutorial-results/blacklist-example \
  --id_file tutorial-results/5-mol2ids.txt \
  --whitelist False
```

    Processing partition_1.mol2 | scanned 10000 molecules | 12772 mol/sec
    Processing partition_2.mol2 | scanned 10000 molecules | 8715 mol/sec
    Processing partition_3.mol2 | scanned 10000 molecules | 9105 mol/sec
    Processing partition_4.mol2 | scanned 10000 molecules | 13333 mol/sec
    Processing partition_5.mol2 | scanned 10000 molecules | 9869 mol/sec
    Processing partition_6.mol2 | scanned 10000 molecules | 12444 mol/sec
    Processing partition_7.mol2 | scanned 10000 molecules | 12276 mol/sec
    Finished


This time, we expect 69995 structures to be obtained after the filtering, since we scanned 70,000 molecules and had 5 molecules on our ID blacklist:


```python
! python tools/count_mol2.py \
  --input tutorial-results/blacklist-example
```

    partition_1.mol2 : 9995
    partition_2.mol2 : 10000
    partition_3.mol2 : 10000
    partition_4.mol2 : 10000
    partition_5.mol2 : 10000
    partition_6.mol2 : 10000
    partition_7.mol2 : 10000
    Total : 69995


## Filtering Step  1 -- Filtering via Features from Data Tables

In this section, we will apply the first filtering step, which constitutes step 1 in the pipeline overview:

![](images/tools-tutorial-1/pipe-step-1.jpg)

Filtering via screenlamp is typically done in 2 steps:

- Step 1: create a ID file containing the names of the molecules of interest
- Step 2: obtain the structures of molecules of interest, using the ID file, from MOL2 files

In this filtering step, we are going to create an ID file of molecules of interest from a pre-existing data table, for instance, the "properties" files available on [ZINC](http://zinc.docking.org/subsets/drug-like). For this example, we are going to use the `small_table_p1-7.txt` subset that we downloaded earlier, since the whole data table of drug like molecules in ~2 Gb in size and may take a long time to download on machines with a low-bandwith internet connection. However, in case you have already downloaded the drug-like properties file (3_prop.xls) please feel free to use it instead. (Note that while `3_prop.xls` has a file ending that is typical for Microsoft Excel, it is not an Excel file but a plain text file with tab-separated columns.)

To get a brief impression of the file contents, we use the `head` tool to display the first 10 entries:


```python
! head tk-tutorial_data/small_table_p1-7.txt
```

    ZINC_ID	MWT	LogP	Desolv_apolar	Desolv_polar	HBD	HBA	tPSA	Charge	NRB	SMILES
    ZINC00000010	217.2	1.42	5.57	-41.98	0	4	66	-1	2	C[C@@]1(C(=O)C=C(O1)C(=O)[O-])c2ccccc2
    ZINC00000012	289.356	1.28	4.89	-24.55	2	4	66	0	5	c1ccc(cc1)C(c2ccccc2)[S@](=O)CC(=O)NO
    ZINC00000017	281.337	1.33	3.06	-23.33	2	6	87	0	4	CCC[S@](=O)c1ccc2c(c1)[nH]/c(=N\C(=O)OC)/[nH]2
    ZINC00000017	281.337	1.33	3.07	-19.2	2	6	87	0	4	CCC[S@](=O)c1ccc2c(c1)[nH]/c(=N/C(=O)OC)/[nH]2
    ZINC00000018	212.31799999999998	2.0	5.87	-8.2	1	3	32	0	4	CC(C)C[C@@H]1C(=O)N(C(=S)N1)CC=C
    ZINC00000021	288.411	3.85	4.02	-40.52	1	3	30	1	6	CCC(=O)O[C@]1(CC[NH+](C[C@@H]1CC=C)C)c2ccccc2
    ZINC00000022	218.27599999999998	3.21	0.47	-48.57	1	3	52	-1	5	C[C@@H](c1ccc(cc1)NCC(=C)C)C(=O)[O-]
    ZINC00000025	251.35299999999998	3.6	2.4	-41.56	2	2	40	1	5	C[C@H](Cc1ccccc1)[NH2+][C@@H](C#N)c2ccccc2
    ZINC00000030	297.422	2.94	0.89	-37.97	3	3	47	1	6	C[C@@H](CC(c1ccccc1)(c2ccccc2)C(=O)N)[NH+](C)C


Using the `datatable_to_id.py` script, we can select only those molecule IDs (or names) (here: stored in the `ZINC_ID` column) that match certain criteria, which we can flexibly define based on the column data in this table. For example, we can select only those molecules that have at most 7 rotatable bonds and have a molecular weight of at least 200 g/mol using the selection string `"(NRB <= 7) & (MWT >= 200)"` as follows:


```python
! python tools/datatable_to_id.py \
  --input tk-tutorial_data/small_table_p1-7.txt \
  --output tutorial-results/01_selected_mol2s.txt \
  --id_column "ZINC_ID" \
  --selection "(NRB <= 7) & (MWT >= 200)"
```

    Using columns: ['ZINC_ID', 'NRB', 'MWT']
    Using selection: (chunk.NRB <= 7) & (chunk.MWT >= 200)
    Processed 169984 rows | 351943 rows/sec
    Selected: 162622


The selection syntax is quite simple: Each criterion must be surrounded by parentheses, and multiple criteria can be chained together using the logical AND symbol `'&'`. For example, to add a third criterion to the selection string to exclude larger molecules that are heavier than 400 g/mol, the selection string becomes `"(NRB <= 7) & (MWT >= 200) & (MWT <= 400)"`.

The operators for comparison allowed:

- `!=` : not equal to
- `==` : equal to
- `<`  : less than
- `>`  : greater than
- `>=` : equal to or greater than
- `<=` : equal to or greater than


If you encounter issues with certain selection strings, please check that the specified column is indeed present in the table you provided. Also, the `datatable_to_id.py` tool assumes that the input table is tab-separated. If you have tables that use a different delimiter to separate columns, please specify the column separator using the `--seperator` parameter. For example, if our input table was a CSV file, we would pass the following, additional argument to the `tools/datatable_to_id.py` function: `--seperator ","`.


Below are some additional examples of correct and incorrect selection strings that can help you with debugging the selection strings if you should encounter problems:

- Correct: `"(MWT >= 200) & (NRB <= 7)"`
- Wrong: `"( MWT >= 200) & ( NRB <= 7)"` [spacing between parentheses and column names]
- Wrong: `"MWT >= 200 & NRB <= 7"` [expressions seperated by logical '&' operator not enclosed in parentheses]
- Wrong: `"(mwt >= 200) & (nrb <= 7)"` [column names don't match the columns in the data table file]
- Wrong: `"(mwt>=200) & (nrb<=7)"` [no whitespace before and after operators for comparison]


As mentioned in the beginning of this section, filtering consists of two steps:
    
1. Creating an ID file of molecule names
2. Selecting molecules from MOL2 files using the ID file from step 1

We already completed step 1, and now, we are going the ID file we just created to create MOL2 files that only contain the molecules of interest (i.e., molecules with a maximum number of 7 rotatable bonds and a molecular weight of at least 200 g/mol2). Consequently, we use the ID file `tutorial-results/01_selected_mol2s.txt` to select the molecules of interest from out MOL2 database at `tk-tutorial_data/partition_1-7/` as follows:


```python
! python tools/id_to_mol2.py \
  --input tk-tutorial_data/partition_1-7/ \
  --output tutorial-results/01_selected_mol2s/ \
  --id_file tutorial-results/01_selected_mol2s.txt \
  --whitelist True
```

    Processing partition_1.mol2 | scanned 10000 molecules | 12021 mol/sec
    Processing partition_2.mol2 | scanned 10000 molecules | 9435 mol/sec
    Processing partition_3.mol2 | scanned 10000 molecules | 7823 mol/sec
    Processing partition_4.mol2 | scanned 10000 molecules | 10801 mol/sec
    Processing partition_5.mol2 | scanned 10000 molecules | 8901 mol/sec
    Processing partition_6.mol2 | scanned 10000 molecules | 8661 mol/sec
    Processing partition_7.mol2 | scanned 10000 molecules | 8167 mol/sec
    Finished



```python
! python tools/count_mol2.py \
  --input tutorial-results/01_selected_mol2s/
```

    partition_1.mol2 : 8628
    partition_2.mol2 : 8501
    partition_3.mol2 : 8537
    partition_4.mol2 : 8476
    partition_5.mol2 : 8535
    partition_6.mol2 : 8518
    partition_7.mol2 : 8555
    Total : 59750


As we can see from the output of `count_mol2.py`, we now have a slightly smaller database consisting of 59750 molecules (selected from the initial 70,000 structures).

## Filtering Step 2 -- Presence and Absence of Functional Groups

In this second filtering steps, we will select molecules that contain certain types of atoms and functional groups. In this simple example, we will consider molecules that contain at least one sp3 sulfur atom (as it can be found in sulfate groups) and at least one sp2 oxygen atom (keto-group). 

![](images/tools-tutorial-1/pipe-step-2.jpg)

When we filter by atom type, we can use the following types to specify filtering criteria:

  - `atom_id`
  - `atom_name`
  - `atom_type`
  - `subst_id`
  - `subst_name`
  - `charge`

Note that the most useful specifiers are `atom_type` and `charge` in the context of selecting atoms and functional groups of interest. The `atom_type` specifier is used to refer to the atom types in MOL2 structures (for example, O.2, O.3, H, S.2, and so forth). The `charge` specify refers to the partial charge column in MOL2 files.

Before we discuss the selection string syntax in more detail, let us execute an example where we select only those molecules that contain at least one sp3 sulfur atom (as it can be found in sulfate groups) and at least one sp2 oxygen atom (keto-group):


```python
! python tools/funcgroup_presence_to_id.py \
  --input tutorial-results/01_selected_mol2s/ \
  --output tutorial-results/02_fgroup_presence_mol2s.txt \
  --selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')" \
  --processes 0
```

    Using selection: ["((pdmol.df.atom_type == 'S.3') | (pdmol.df.atom_type == 'S.o2'))", "(pdmol.df.atom_type == 'O.2')"]
    Processing partition_1.mol2 | 231 mol/sec
    Processing partition_2.mol2 | 260 mol/sec
    Processing partition_3.mol2 | 277 mol/sec
    Processing partition_4.mol2 | 256 mol/sec
    Processing partition_5.mol2 | 268 mol/sec
    Processing partition_6.mol2 | 279 mol/sec
    Processing partition_7.mol2 | 277 mol/sec


Note that the we use all available processes on our machine by setting `--processes 0`, to speed up the computation. Alternatively, if you don't want to utilize all available CPUs, you can specify the number of CPUs to use manually, for example, by setting `--processes 1` to only use 1 CPU.

To better understand how the selection string "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')" works, let us break it down into 2 parts:

1. "((atom_type == 'S.3') | (atom_type == 'S.o2'))"
2. "--> (atom_type == 'O.2')"
    
In the first part, we use the logical OR operator '|' to select molecules that either contain an 'S.3' atom OR an 'S.o2' atom. Then, after this criterion has been applied to select the specified subset of molecules, the next criterion will be applied, the criterion followed by the '-->' string. In this case, the second criterion is to check the remaining molecules for the presence of an 'O.2' atom. In this context, you can think of the '-->' string as a "THEN" conditional statement. E.g., "select via filter ((atom_type == 'S.3') | (atom_type == 'S.o2')) THEN select via filter (atom_type == 'O.2')"


Note that you can string an arbitrary number of criteria using the '-->' operator. For example, if we additionally require molecules to contain a fluor atom, we can modify the selection string as follows:

"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2') **--> (atom_type == 'F')**"

Lastly, we can also incorporate partial charge information. For instance if we want to specify a partial charge range for the O.2 atom type, we could do it as follows, using the logical "&" operator:

"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> ((atom_type == 'O.2') **& (charge <= -0.3) & (charge >= -0.9))**"

Please note that it doesn't make sense to use the logical AND operator (&) on the same column. For example, the selection string "((atom_type == 'S.3') | (atom_type == 'S.o2'))" means that a molecule must contain an atom that is either of type S.3 OR S.o2. However, the selection string "((atom_type == 'S.3') & (atom_type == 'S.o2'))" would mean that a molecule must contain an atom that has the type S.3 AND S.o2, which is impossible, because an atom can only have 1 type at the same time (in the MOL2 file format).


---

**Below, you can find a short list of Dos and Don'ts regarding the selection syntax**:

a) Don't use the AND operator (&) on the same column within a selection: "((atom_type == 'S.3') | (atom_type == 'S.o2')) & (atom_type == 'O.2')"

- This selects molecules with an S.3 or S.o2 atom that is also an O.2 atom at the same time. This is impossible!

b) Use the AND operator on different columns within a slection: "((atom_type == 'S.3') | (atom_type == 'S.o2')) & (charge < 0.0)"

- This selects molecules with an S.3 or S.o2 atom that also has a negative charge.

c) Filter for multiple atoms by chaining criteria via the `-->` string: "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"

- This selects molecules with an S.3 or S.o2 atom. Then, based on those molecules, it selects only those molecules that also contain an O.2 atom.

---

As you remember from the "Filtering Step 1" section, filtering in screenlamp concists of two steps:

1. Creating an ID file of molecule names
2. Selecting molecules from MOL2 files using the ID file from step 1

We have already completed step 1 so that we can use the ID file we created to select the MOL2 structures from the MOL2 directory as follows:


```python
! python tools/id_to_mol2.py \
  --input tutorial-results/01_selected_mol2s/ \
  --output tutorial-results/02_fgroup_presence_mol2s \
  --id_file tutorial-results/02_fgroup_presence_mol2s.txt \
  --whitelist True
```

    Processing partition_1.mol2 | scanned 8628 molecules | 13872 mol/sec
    Processing partition_2.mol2 | scanned 8501 molecules | 12075 mol/sec
    Processing partition_3.mol2 | scanned 8537 molecules | 9794 mol/sec
    Processing partition_4.mol2 | scanned 8476 molecules | 12817 mol/sec
    Processing partition_5.mol2 | scanned 8535 molecules | 15391 mol/sec
    Processing partition_6.mol2 | scanned 8518 molecules | 12703 mol/sec
    Processing partition_7.mol2 | scanned 8555 molecules | 11566 mol/sec
    Finished



```python
! python tools/count_mol2.py \
--input tutorial-results/02_fgroup_presence_mol2s
```

    partition_1.mol2 : 2140
    partition_2.mol2 : 2118
    partition_3.mol2 : 2064
    partition_4.mol2 : 2107
    partition_5.mol2 : 2068
    partition_6.mol2 : 2189
    partition_7.mol2 : 2186
    Total : 14872


As we can see, we only have 14,872 by applying the atom- and functional group based selection criteria. To summarize the steps so far, in "Filtering Step 1" we selected 59,750 (molecules that have fewer than 7 rotatable bonds and are heavier than 200 g/mol) out of 70,000 molecules. Then, in this section ("Filtering Step 2"), we selected 14,872 out of those 59,750, molecules that have at least 1 keto and 1 sp3 sulfur atom.

## Filtering Step 3 -- Distance between functional groups

In this step, we will now select only those molecules that have a sp3 sulfur atom and a keto-group within a 13-20 angstrom distance:

![](images/tools-tutorial-1/pipe-step-3.jpg)

Technically, we could have skipped the section "Filtering Step 2" and directly proceeded with the distance-based atom selection described in this section. However, note that distance calculations are computationally more expensive than merely checking for the presence of certain atoms and functional groups. Thus, but separating those two tasks, we can filter out molecules that don't contain a keto and a sp3 sulfur atoms first.

The selection string syntax is analagous to the `--selection` parameter described in the "Filtering Step 2" --  please re-visit this section if you need a refresher. However, it shall be noted that the distance selection only works for a pair of atoms. For example, the following string

"((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"

checks the distance between an atom A, which is either an S.3 or an S.o2 atom, and an atom B, which is a O.2 atom. If you want to compute the distance between multiple atoms, for example, the distance of atom A to atoms B and C, you need to repeat the distance selection multiple times. For example, you would perform the distance selection between A and B first, and then, in a second iteration, you would perform the distance selection on the results of the first selection, to select molecules based on the distance between atom A and C.

Now, let us execute the first step of a filtering step in screenlamp and create an ID file of molecules that have an sp3 sulfur and a O.2 atom within a 13-20 angstrom distance. 


```python
! python tools/funcgroup_distance_to_id.py \
  --input tutorial-results/02_fgroup_presence_mol2s \
  --output tutorial-results/03_fgroup_distance_mol2s.txt \
  --selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')" \
  --distance "13-20" \
  --processes 0
```

    Using selection: ["((pdmol.df.atom_type == 'S.3') | (pdmol.df.atom_type == 'S.o2'))", "(pdmol.df.atom_type == 'O.2')"]
    Processing partition_1.mol2 | 200 mol/sec
    Processing partition_2.mol2 | 193 mol/sec
    Processing partition_3.mol2 | 154 mol/sec
    Processing partition_4.mol2 | 212 mol/sec
    Processing partition_5.mol2 | 160 mol/sec
    Processing partition_6.mol2 | 209 mol/sec
    Processing partition_7.mol2 | 206 mol/sec


Following the already familiar procedure, we can now select the MOL2 structures using the generated ID file:


```python
! python tools/id_to_mol2.py \
  --input tutorial-results/02_fgroup_presence_mol2s \
  --output tutorial-results/03_fgroup_distance_mol2s \
  --id_file tutorial-results/03_fgroup_distance_mol2s.txt \
  --whitelist True
```

    Processing partition_1.mol2 | scanned 2140 molecules | 12000 mol/sec
    Processing partition_2.mol2 | scanned 2118 molecules | 10976 mol/sec
    Processing partition_3.mol2 | scanned 2064 molecules | 11510 mol/sec
    Processing partition_4.mol2 | scanned 2107 molecules | 12223 mol/sec
    Processing partition_5.mol2 | scanned 2068 molecules | 15665 mol/sec
    Processing partition_6.mol2 | scanned 2189 molecules | 10884 mol/sec
    Processing partition_7.mol2 | scanned 2186 molecules | 15554 mol/sec
    Finished



```python
!python tools/count_mol2.py \
--input tutorial-results/03_fgroup_distance_mol2s
```

    partition_1.mol2 : 16
    partition_2.mol2 : 16
    partition_3.mol2 : 13
    partition_4.mol2 : 15
    partition_5.mol2 : 12
    partition_6.mol2 : 20
    partition_7.mol2 : 15
    Total : 107


After applying this filtering step, we can see that only 107 molecules out of the 14,872 from "Filtering Step 2" remain.

# Generating Conformers via Omega


```python
! python ../../../../tools/run_omega.py \
--input project/prefilter_3/3keto-and-sulfur_distance-mol2s \
--output project/omega_confomers/ \
--executable "/Applications/OMEGA 2.5.1.4.app/Contents/MacOS/omega2-2.5.1.4" \
--processes 0
```

    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Running as MPI Master
    ...fur_distance-mol2s/1.mol2|****************************************|100.00%
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Running as MPI Master
    ...fur_distance-mol2s/2.mol2|****************************************|100.00%
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Slave started on host Sebastians-MacBook-Pro
    Running as MPI Master
    ...fur_distance-mol2s/3.mol2|****************************************|100.00%
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
    Slave started on host Sebastians-MacBook-Pro
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Running as MPI Master
    ...fur_distance-mol2s/4.mol2|****************************************|100.00%
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Slave started on host Sebastians-MacBook-Pro
    Running as MPI Master
    ...fur_distance-mol2s/5.mol2|****************************************|100.00%
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Running as MPI Master
    ...fur_distance-mol2s/6.mol2|****************************************|100.00%
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    
              :jGf:             .d8888b. 88d8b.d8b. .d8888b. .d8888b. .d8888b.
            :jGDDDDf:           88'  `88 88'`88'`88 88ooood8 88'  `88 88'  `88
          ,fDDDGjLDDDf,         88.  .88 88  88  88 88.  ... 88.  .88 88.  .88
        ,fDDLt:   :iLDDL;       `88888P' dP  dP  dP `88888P' `8888P88 `88888P8
      ;fDLt:         :tfDG;                                       .88
    ,jft:   ,ijfffji,   :iff                                  d8888P
         .jGDDDDDDDDDGt.      
        ;GDDGt:''':tDDDG,          Copyright (c) 2004-2013
       .DDDG:       :GDDG.         OpenEye Scientific Software, Inc.
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Version: 2.5.1.4
        LDDDt.     .fDDDj          Built:   20130515
        .tDDDDfjtjfDDDGt           OEChem version: 1.9.1
          :ifGDDDDDGfi.            Platform: osx-10.8-clang++4-x64
    Slave started on host Sebastians-MacBook-Pro
              .:::.                
      ......................       
      DDDDDDDDDDDDDDDDDDDDDD       
      DDDDDDDDDDDDDDDDDDDDDD       
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite OMEGA please use the following:
      OMEGA 2.5.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Warren, G.L.; Ellingson, B.A.; Stahl, M.T.
      Conformer Generation with OMEGA: Algorithm and Validation Using High
      Quality Structures from the Protein Databank and the Cambridge 
      Structural Database. J. Chem. Inf. Model. 2010, 50, 572-584.
    
    Running as MPI Master
    ...fur_distance-mol2s/7.mol2|****************************************|100.00%



```python
!python ../../../../tools/count_mol2.py \
--input project/omega_confomers/
```

    1.mol2 : 6531
    2.mol2 : 5840
    3.mol2 : 6686
    4.mol2 : 7402
    5.mol2 : 5987
    6.mol2 : 5833
    7.mol2 : 6725
    Total : 45004


# Overlaying conformers with query using ROCS


```python
!python ../../../../tools/run_rocs.py \
--input project/omega_confomers \
--output project/rocs_overlays/ \
--query dataset/query/3kpzs_conf_subset_nowarts.mol2 \
--executable "/Applications/ROCS 3.2.1.4.app/Contents/MacOS/rocs-3.2.1.4" \
--processes 0
```

    Processing 1.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/1.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/1
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/1.log
    Statistics will be written to:	project/rocs_overlays_nowarts/1_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/1_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/1_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/1.mol2
    ...ct/omega_confomers/1.mol2|****************************************|100.00%
    
    35 molecules in 67 seconds -> 0.5 molecules/sec
                                  3412 overlays/sec
    
    35 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1
    Processing 2.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/2.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/2
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/2.log
    Statistics will be written to:	project/rocs_overlays_nowarts/2_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/2_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/2_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/2.mol2
    ...ct/omega_confomers/2.mol2|****************************************|100.00%
    
    32 molecules in 59 seconds -> 0.5 molecules/sec
                                  3464 overlays/sec
    
    32 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1
    Processing 3.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/3.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/3
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/3.log
    Statistics will be written to:	project/rocs_overlays_nowarts/3_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/3_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/3_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/3.mol2
    ...ct/omega_confomers/3.mol2|****************************************|100.00%
    
    38 molecules in 75 seconds -> 0.5 molecules/sec
                                  3120 overlays/sec
    
    38 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1
    Processing 4.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/4.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/4
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/4.log
    Statistics will be written to:	project/rocs_overlays_nowarts/4_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/4_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/4_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/4.mol2
    ...ct/omega_confomers/4.mol2|****************************************|100.00%
    
    40 molecules in 82 seconds -> 0.5 molecules/sec
                                  3159 overlays/sec
    
    40 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1
    Processing 5.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/5.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/5
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/5.log
    Statistics will be written to:	project/rocs_overlays_nowarts/5_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/5_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/5_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/5.mol2
    ...ct/omega_confomers/5.mol2|****************************************|100.00%
    
    32 molecules in 67 seconds -> 0.5 molecules/sec
                                  3128 overlays/sec
    
    32 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1
    Processing 6.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/6.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/6
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/6.log
    Statistics will be written to:	project/rocs_overlays_nowarts/6_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/6_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/6_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/6.mol2
    ...ct/omega_confomers/6.mol2|****************************************|100.00%
    
    32 molecules in 68 seconds -> 0.5 molecules/sec
                                  3002 overlays/sec
    
    32 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1
    Processing 7.mol2
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
    Slave started on host Sebastians-MacBook-Pro
              :jGf:               
            :jGDDDDf:             
          ,fDDDGjLDDDf,           'a8  ,a'8b   a''8b    a''8b  a8f'8
        ,fDDLt:   :iLDDL;          88 a/  88  d'   8b  d'  88  88'  
      ;fDLt:         :tfDG;        88P    8f d8    88 d8       '88aa
    ,jft:   ,ijfffji,   :iff       8P        88    8P 88      a  '888
         .jGDDDDDDDDDGt.           8i        88   d8  Y8   ,d 8    8P
        ;GDDGt:''':tDDDG,          a8/        `88aa'    '8aa'  'baa8'
       .DDDG:       :GDDG.    
       ;DDDj         tDDDi    
       ,DDDf         fDDD,         Copyright (C) 1997-2015
        LDDDt.     .fDDDj          OpenEye Scientific Software, Inc.
        .tDDDDfjtjfDDDGt      
          :ifGDDDDDGfi.            Version: 3.2.1.4
              .:::.                Built:   20150831
      ......................       OEChem version: 2.0.4
      DDDDDDDDDDDDDDDDDDDDDD       Platform: osx-10.10-clang++6-x64
      DDDDDDDDDDDDDDDDDDDDDD  
    
    Supported run modes:
      Single processor
      MPI Multiprocessor
    
      Licensed for the exclusive use of The Laboratory of Leslie Kuhn.
      Licensed for use only in Michigan State University.
      License expires on October 20, 2017.
    
    
    To cite ROCS please use the following:
      ROCS 3.2.1.4: OpenEye Scientific Software, Santa Fe, NM.
      http://www.eyesopen.com.
    
      Hawkins, P.C.D.; Skillman, A.G.; Nicholls, A. Comparison of Shape-Matching
      and Docking as Virtual Screening Tools. J. Med. Chem., 2007, 50, 74.
    
    Running as MPI Master
      database file: project/omega_confomers/7.mol2
    
    Query being read from:         	dataset/query/3kpzs_conf_subset_nowarts.mol2
    File prefix is:                	project/rocs_overlays_nowarts/7
    Output directory:              	/Users/sebastian/code/screenlamp/docs/sources/workflow/example_1
    Log file will be written to: 	project/rocs_overlays_nowarts/7.log
    Statistics will be written to:	project/rocs_overlays_nowarts/7_1.rpt
    Hit structures will written to:	project/rocs_overlays_nowarts/7_hits_1.mol2
    Status file will be written to:	project/rocs_overlays_nowarts/7_1.status
    
    Query(#1): 3KPZS has 35 conformer(s)
    Database 1 of 1:              	project/omega_confomers/7.mol2
    ...ct/omega_confomers/7.mol2|****************************************|100.00%
    
    37 molecules in 75 seconds -> 0.5 molecules/sec
                                  3138 overlays/sec
    
    37 hits found
    =================================================
    
    Molecule read failures: 0
    #warnings             : 0
    #errors               : 0
    #queries processed    : 1



```python
!python ../../../../tools/count_mol2.py \
--input project/rocs_overlays/
```

    1_hits_1.mol2 : 35
    2_hits_1.mol2 : 32
    3_hits_1.mol2 : 38
    4_hits_1.mol2 : 40
    5_hits_1.mol2 : 32
    6_hits_1.mol2 : 32
    7_hits_1.mol2 : 37
    Total : 246


- After ROCS, we can sort the output files to create mol2 files with the overlays in sorted order by score

- a) a mol2 file that contains the database molecule conformers in sort order
- b) a mol2 files with the corresponding query conformers

using `sort_rocs_mol2.py`


```python
!python ../../../../tools/sort_rocs_mol2.py \
--input project/rocs_overlays/ \
--output project/rocs_overlays_sorted \
--query ./dataset/query/3kpzs_conf_subset_nowarts.mol2 \
--sortby TanimotoCombo \
--id_suffix true
```

    Processing 1_hits_1.mol2 | scanned 36 molecules | 1663 mol/sec
    Processing 2_hits_1.mol2 | scanned 33 molecules | 4204 mol/sec
    Processing 3_hits_1.mol2 | scanned 39 molecules | 7292 mol/sec
    Processing 4_hits_1.mol2 | scanned 41 molecules | 7170 mol/sec
    Processing 5_hits_1.mol2 | scanned 33 molecules | 7686 mol/sec
    Processing 6_hits_1.mol2 | scanned 33 molecules | 7354 mol/sec
    Processing 7_hits_1.mol2 | scanned 38 molecules | 4984 mol/sec


- these can then be opened and viewed in pymol

# Matching Functional Groups

will need suffixes:

- _dbase.mol2 / _dbase.mol2.gz and 
- _query.mol2 / _query.mol2.gz and 


```python
!python ../../../../tools/funcgroup_matching.py \
--input project/rocs_overlays_sorted \
--output project/funcgroup_matching_results \
--max_distance 1.3 \
--processes 0
```

    Processing 1_hits_1_dbase.mol2/1_hits_1_query.mol2 | scanned 36 molecules | 33 mol/sec
    Processing 2_hits_1_dbase.mol2/2_hits_1_query.mol2 | scanned 33 molecules | 38 mol/sec
    Processing 3_hits_1_dbase.mol2/3_hits_1_query.mol2 | scanned 39 molecules | 41 mol/sec
    Processing 4_hits_1_dbase.mol2/4_hits_1_query.mol2 | scanned 41 molecules | 38 mol/sec
    Processing 5_hits_1_dbase.mol2/5_hits_1_query.mol2 | scanned 33 molecules | 34 mol/sec
    Processing 6_hits_1_dbase.mol2/6_hits_1_query.mol2 | scanned 33 molecules | 31 mol/sec
    Processing 7_hits_1_dbase.mol2/7_hits_1_query.mol2 | scanned 38 molecules | 32 mol/sec


# TODO


```python

```
