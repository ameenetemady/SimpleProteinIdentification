# Simple Protein Inference #

### Dependencies
* python3.4 or above
* [biopython](http://biopython.org/wiki/Download)

### Installation
git clone https://github.com/ameenetemady/H

### Running
* Step1: prepare a directory containing your input files (with exact names):

  * ```identification.tsv```: tab-delimeted file:  **column1**: peptide, **column2**: protein name, **column3**: identification probability
  * ```db.fasta```: reference protein database in fasta format.

* Step2: ```python run.py directoryName```

Upon completion, ```pred.csv``` will contain the predicted protein identification probabilities.

### Benchmark Datasets
There are [7 example datasets](https://github.com/ameenetemady/H/tree/master/data) available in this repository.
