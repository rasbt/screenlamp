# Data storage and project layout

- The initial dataset should be stored as `mol2` or `mol2.gz` files in a directory. For example:


```python
!ls -lh dataset/mol2/
```

    total 603744
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 1.mol2
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 2.mol2
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 3.mol2
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 4.mol2
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 5.mol2
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 6.mol2
    -rw-r--r--  1 sebastian  staff    42M May 10 22:41 7.mol2


- for a new project, it's best to create a new directory, for instance, we create a new subdirectory in 80698:


```python
!mkdir project
```

    mkdir: project: File exists


Using the `count_mol2.py` script, we can count the number of structures in each mol2 file in the input directory:


```python
!python ../../../../tools/count_mol2.py -i dataset/mol2/
```

    1.mol2 : 10000
    2.mol2 : 10000
    3.mol2 : 10000
    4.mol2 : 10000
    5.mol2 : 10000
    6.mol2 : 10000
    7.mol2 : 10000
    Total : 70000


Optionally, you may have files with data about the molecules, for instance:


```python
!ls -lh dataset/tables
```

    total 3310280
    -rw-r--r--@ 1 sebastian  staff   1.6G Jan 11  2014 3_prop.xls


# General Blacklist & Whitelist filtering

- `mol2_to_id.py` generates a list of molecule IDs from MOL2 files
- `id_to_mol2.py` filters mol2 files by IDs and creates new mol2 files. Via whitelisting, molecules that match those IDs are written. Via blacklisting, all molecules but the molecules that are in the list are written


```python
!python ../../../../tools/mol2_to_id.py \
--input dataset/mol2 \
--output project/all-mol2ids.txt
```

    Processing 1.mol2 | scanned 10000 molecules | 12824 mol/sec
    Processing 2.mol2 | scanned 10000 molecules | 12196 mol/sec
    Processing 3.mol2 | scanned 10000 molecules | 12604 mol/sec
    Processing 4.mol2 | scanned 10000 molecules | 14002 mol/sec
    Processing 5.mol2 | scanned 10000 molecules | 15695 mol/sec
    Processing 6.mol2 | scanned 10000 molecules | 16035 mol/sec
    Processing 7.mol2 | scanned 10000 molecules | 16698 mol/sec



```python
!head project/all-mol2ids.txt
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


- Say we are interested in a subset of molecules only. Consider this example: 1st we create a list of IDs:


```python
%%writefile project/random-sample-of-mol2ids.txt
ZINC65255333
ZINC06394508
ZINC65292537
ZINC65375610
ZINC31820077
```

    Overwriting project/random-sample-of-mol2ids.txt


### Whitelisting


```python
!python ../../../../tools/id_to_mol2.py \
--input dataset/mol2 \
--output project/random-sample-of-mol2ids_mol2s_1 \
--id_file project/random-sample-of-mol2ids.txt \
--whitelist True
```

    Processing 1.mol2 | scanned 10000 molecules | 17030 mol/sec
    Processing 2.mol2 | scanned 10000 molecules | 17095 mol/sec
    Processing 3.mol2 | scanned 10000 molecules | 17176 mol/sec
    Processing 4.mol2 | scanned 10000 molecules | 16746 mol/sec
    Processing 5.mol2 | scanned 10000 molecules | 17894 mol/sec
    Processing 6.mol2 | scanned 10000 molecules | 17808 mol/sec
    Processing 7.mol2 | scanned 10000 molecules | 17681 mol/sec
    Finished


Now, the output directory, `80698/proj-1/selected-example-mol2ids`, should contain only mol2 files with the selected IDs:


```python
!ls project/random-sample-of-mol2ids_mol2s_1
```

    1.mol2 2.mol2 3.mol2 4.mol2 5.mol2 6.mol2 7.mol2



```python
!python ../../../../tools/count_mol2.py \
--input project/random-sample-of-mol2ids_mol2s_1
```

    1.mol2 : 5
    2.mol2 : 0
    3.mol2 : 0
    4.mol2 : 0
    5.mol2 : 0
    6.mol2 : 0
    7.mol2 : 0
    Total : 5


### Blacklisting

Similar to the previous approach, using a whitelist filter, we can do blacklist filtering, which means that all molecules are selected but the ones contained in the ID files. Set whitelist to False.


```python
!python ../../../../tools/id_to_mol2.py \
--input dataset/mol2 \
--output project/random-sample-of-mol2ids_mol2s_2 \
--id_file project/random-sample-of-mol2ids.txt \
--whitelist False
```

    Processing 1.mol2 | scanned 10000 molecules | 14094 mol/sec
    Processing 2.mol2 | scanned 10000 molecules | 13256 mol/sec
    Processing 3.mol2 | scanned 10000 molecules | 13598 mol/sec
    Processing 4.mol2 | scanned 10000 molecules | 12648 mol/sec
    Processing 5.mol2 | scanned 10000 molecules | 12714 mol/sec
    Processing 6.mol2 | scanned 10000 molecules | 12869 mol/sec
    Processing 7.mol2 | scanned 10000 molecules | 12863 mol/sec
    Finished



```python
!python ../../../../tools/count_mol2.py -i project/random-sample-of-mol2ids_mol2s_2
```

    1.mol2 : 9995
    2.mol2 : 10000
    3.mol2 : 10000
    4.mol2 : 10000
    5.mol2 : 10000
    6.mol2 : 10000
    7.mol2 : 10000
    Total : 69995


# First Filtering Step -- Filtering via Features from Data Tables


```python
!head dataset/tables/3_prop.xls
```

    ZINC_ID	MWT	LogP	Desolv_apolar	Desolv_polar	HBD	HBA	tPSA	Charge	NRB	SMILES
    ZINC00000010	217.2	1.42	5.57	-41.98	0	4	66	-1	2	C[C@@]1(C(=O)C=C(O1)C(=O)[O-])c2ccccc2
    ZINC00000012	289.356	1.28	4.89	-24.55	2	4	66	0	5	c1ccc(cc1)C(c2ccccc2)[S@](=O)CC(=O)NO
    ZINC00000017	281.337	1.33	3.06	-23.33	2	6	87	0	4	CCC[S@](=O)c1ccc2c(c1)[nH]/c(=N\C(=O)OC)/[nH]2
    ZINC00000017	281.337	1.33	3.07	-19.2	2	6	87	0	4	CCC[S@](=O)c1ccc2c(c1)[nH]/c(=N/C(=O)OC)/[nH]2
    ZINC00000018	212.318	2.00	5.87	-8.2	1	3	32	0	4	CC(C)C[C@@H]1C(=O)N(C(=S)N1)CC=C
    ZINC00000021	288.411	3.85	4.02	-40.52	1	3	30	1	6	CCC(=O)O[C@]1(CC[NH+](C[C@@H]1CC=C)C)c2ccccc2
    ZINC00000022	218.276	3.21	0.47	-48.57	1	3	52	-1	5	C[C@@H](c1ccc(cc1)NCC(=C)C)C(=O)[O-]
    ZINC00000025	251.353	3.60	2.4	-41.56	2	2	40	1	5	C[C@H](Cc1ccccc1)[NH2+][C@@H](C#N)c2ccccc2
    ZINC00000030	297.422	2.94	0.89	-37.97	3	3	47	1	6	C[C@@H](CC(c1ccccc1)(c2ccccc2)C(=O)N)[NH+](C)C


- A valid query looks like this:
 
- Correct: `"(MWT >= 200) & (NRB <= 7)"`
- Wrong: `"( MWT >= 200) & ( NRB <= 7)"` [spacing between parentheses and column names]
- Wrong: `"MWT >= 200 & NRB <= 7"` [expressions seperated by logical '&' operator not enclosed in parentheses]
- Wrong: `"(mwt >= 200) & (nrb <= 7)"` [column names don't match the columns in the data table file]
- Wrong: `"(mwt>=200) & (nrb<=7)"` [no whitespace before and after operators for comparison]



```python
!python ../../../../tools/datatable_to_id.py \
--input dataset/tables/3_prop.xls \
--output project/prefilter_1/selected-mol2ids.txt \
--id_column ZINC_ID \
--selection "(NRB <= 7) & (MWT >= 200)"
```

    Using columns: ['ZINC_ID', 'NRB', 'MWT']
    Using selection: (chunk.NRB <= 7) & (chunk.MWT >= 200)
    Processed 18000000 rows | 355868 rows/sec
    Selected: 17599186


Next, we are going to use these IDs to select molecules from the existing mol2 files:


```python
!python ../../../../tools/id_to_mol2.py \
--input dataset/mol2 \
--output project/prefilter_1/selected-mol2s \
--id_file project/prefilter_1/selected-mol2ids.txt \
--whitelist True
```

    Processing 1.mol2 | scanned 10000 molecules | 12869 mol/sec
    Processing 2.mol2 | scanned 10000 molecules | 9978 mol/sec
    Processing 3.mol2 | scanned 10000 molecules | 10434 mol/sec
    Processing 4.mol2 | scanned 10000 molecules | 12147 mol/sec
    Processing 5.mol2 | scanned 10000 molecules | 12625 mol/sec
    Processing 6.mol2 | scanned 10000 molecules | 13190 mol/sec
    Processing 7.mol2 | scanned 10000 molecules | 13364 mol/sec
    Finished



```python
!python ../../../../tools/count_mol2.py \
--input project/prefilter_1/selected-mol2s/
```

    1.mol2 : 9829
    2.mol2 : 9799
    3.mol2 : 9848
    4.mol2 : 9835
    5.mol2 : 9832
    6.mol2 : 9841
    7.mol2 : 9841
    Total : 68825


# Second Filtering Step -- Presence and absence of functional groups

- allowed columns
  - atom_id
  - atom_name
  - atom_type
  - subst_id
  - subst_name
  - charge
  
(may change with updated biopandas)

a) simultaneously true (here impossible): "((atom_type == 'S.3') | (atom_type == 'S.o2')) & (atom_type == 'O.2')"

- tries to find an S.3 or S.o2 atom that is also an O.2 atom at the same time

b) simultaneously true and valid: "((atom_type == 'S.3') | (atom_type == 'S.o2')) & (charge < 0.0)"

- tries to find an S.3 or S.o2 atom that has a negative charge

c) otherwise, "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')"

- tries to find an S.3 or S.o2 atom, then tries to find an O.2 atom as well

d) when in doubt, one can run (as alternative for c) the tool 2 times. 1 time to select "(atom_type == 'S.3') | (atom_type == 'S.o2')" and a second time to select "(atom_type == 'O.2')".


```python
!python ../../../../tools/funcgroup_to_id.py \
--input project/prefilter_1/selected-mol2s/ \
--output project/prefilter_2/3keto-and-sulfur-mol2ids.txt \
--selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')" \
--processes 0
```

    Using selection: ["((pdmol.df.atom_type == 'S.3') | (pdmol.df.atom_type == 'S.o2'))", "(pdmol.df.atom_type == 'O.2')"]
    Processing 1.mol2 | 351 mol/sec
    Processing 2.mol2 | 364 mol/sec
    Processing 3.mol2 | 348 mol/sec
    Processing 4.mol2 | 329 mol/sec
    Processing 5.mol2


```python
!python ../../../../tools/id_to_mol2.py \
--input project/prefilter_1/selected-mol2s \
--output  project/prefilter_2/3keto-and-sulfur-mol2s \
--id_file project/prefilter_2/3keto-and-sulfur-mol2ids.txt \
--whitelist True
```

    Processing 1.mol2 | scanned 9829 molecules | 12209 mol/sec
    Processing 2.mol2 | scanned 9799 molecules | 15392 mol/sec
    Processing 3.mol2 | scanned 9848 molecules | 12854 mol/sec
    Processing 4.mol2 | scanned 9835 molecules | 11223 mol/sec
    Processing 5.mol2 | scanned 9832 molecules | 12398 mol/sec
    Processing 6.mol2 | scanned 9841 molecules | 12885 mol/sec
    Processing 7.mol2 | scanned 9841 molecules | 12163 mol/sec
    Finished



```python
!python ../../../../tools/count_mol2.py \
--input project/prefilter_2/3keto-and-sulfur-mol2s
```

    1.mol2 : 2768
    2.mol2 : 2795
    3.mol2 : 2746
    4.mol2 : 2847
    5.mol2 : 2723
    6.mol2 : 2859
    7.mol2 : 2815
    Total : 19553


# Third Filtering Step -- Distance between functional groups

- could be done after omega


```python
!python ../../../../tools/funcgroup_distance_to_id.py \
--input project/prefilter_2/3keto-and-sulfur-mol2s \
--output project/prefilter_3/3keto-and-sulfur_distance-mol2ids.txt \
--selection "((atom_type == 'S.3') | (atom_type == 'S.o2')) --> (atom_type == 'O.2')" \
--distance "13-20" \
--processes 0
```

    Using selection: ["((pdmol.df.atom_type == 'S.3') | (pdmol.df.atom_type == 'S.o2'))", "(pdmol.df.atom_type == 'O.2')"]
    Processing 1.mol2 | 233 mol/sec
    Processing 2.mol2 | 217 mol/sec
    Processing 3.mol2 | 222 mol/sec
    Processing 4.mol2 | 226 mol/sec
    Processing 5.mol2 | 235 mol/sec
    Processing 6.mol2 | 208 mol/sec
    Processing 7.mol2 | 228 mol/sec



```python
!python ../../../../tools/id_to_mol2.py \
--input project/prefilter_2/3keto-and-sulfur-mol2s \
--output project/prefilter_3/3keto-and-sulfur_distance-mol2s \
--id_file project/prefilter_3/3keto-and-sulfur_distance-mol2ids.txt \
--whitelist True
```

    Processing 1.mol2 | scanned 2768 molecules | 15635 mol/sec
    Processing 2.mol2 | scanned 2795 molecules | 14949 mol/sec
    Processing 3.mol2 | scanned 2746 molecules | 14531 mol/sec
    Processing 4.mol2 | scanned 2847 molecules | 15620 mol/sec
    Processing 5.mol2 | scanned 2723 molecules | 15973 mol/sec
    Processing 6.mol2 | scanned 2859 molecules | 15512 mol/sec
    Processing 7.mol2 | scanned 2815 molecules | 16004 mol/sec
    Finished



```python
!python ../../../../tools/count_mol2.py \
--input project/prefilter_3/3keto-and-sulfur_distance-mol2s
```

    1.mol2 : 35
    2.mol2 : 32
    3.mol2 : 38
    4.mol2 : 40
    5.mol2 : 32
    6.mol2 : 32
    7.mol2 : 37
    Total : 246


# Generating Conformers via Omega


```python
!python ../../../../tools/run_omega.py \
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
