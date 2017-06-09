# Automated Pipeline Tutorial

## Overview

This tutorial explains how to use a pre-built screenlamp pipeline to perform an automated virtual screening on a small example dataset.


## Obtaining and Preparing the Dataset


### MOL2 Input Files

The dataset that we are using consists of 70,000 small molecules split into 7 multi-MOL2 file with 10,000 molecules each: `partition_mol2_1.mol2` to `partition_mol2_7.mol2`. For this tutorial, please download the dataset by clicking the following link and unzip it on your machine that you are using for the virtual screening run: [https://s3-us-west-2.amazonaws.com/screenlamp-datasets/partition_1-7.zip](https://s3-us-west-2.amazonaws.com/screenlamp-datasets/partition_1-7.zip)

### Datatable for Prefiltering

For this particular tutorial you'll also need a datatable containing general information about these molecules. Although the partitions you downloaded above are only a small, modified subset of [ZINC](http://zinc.docking.org) molecules, we are going to use the full ~18,000,000 molecule Drug-like table available for download at [http://zinc.docking.org/subsets/drug-like](http://zinc.docking.org/subsets/drug-like). To download this table, click on the [Properties](http://zinc.docking.org/db/bysubset/3/3_prop.xls) link on the [ZINC Drug-like](http://zinc.docking.org/subsets/drug-like) page.


### Query Molecule

The third datafile you'll need for ligand-based virtual screening is the query molecule. For this tutorial, please download the following multi-conformer MOL2 file: [https://s3-us-west-2.amazonaws.com/screenlamp-datasets/3kpzs_query.mol2](https://s3-us-west-2.amazonaws.com/screenlamp-datasets/3kpzs_query.mol2)

## Editing the Configuration File

Once you obtained the database molecules (mol2 partitions), the datatable of molecular properties, and the query molecule, you can prepare the configuration file that stores the information about your local file paths and screening settings.

python ~/code/screenlamp/tools/pipelines/pipeline-example-1.py -c ~/code/screenlamp/tools/pipelines/pipeline-example-1-config.yaml  --interactive true