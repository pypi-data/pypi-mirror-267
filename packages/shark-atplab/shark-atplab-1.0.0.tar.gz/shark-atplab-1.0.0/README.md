# SHARK (Similarity/Homology Assessment by Relating K-mers)
________________

To accurately assess homology between unalignable sequences, we developed an alignment-free sequence comparison algorithm, SHARK (Similarity/Homology Assessment by Relating K-mers). 

##  SHARK-dive 

We trained SHARK-dive, a machine learning homology classifier, which achieved superior performance to standard alignment in assessing homology in unalignable sequences, and correctly identified dissimilar IDRs capable of functional rescue in IDR-replacement experiments reported in the literature.

### 1. Dive-Score
Scoring the similarity between a pair of sequence

Variants:
   1. Normal (`SHARK-score (T)`)
   2. Sparse (`SHARK-score (best)`)

### 2. Dive-Predict
Find sequences similar to a given query from a target set   


## User Section

### Installation
________________________

**[Recommended]** Use within a local python virtual environment
`python -m venv /path/to/new/virtual/environment`

Current recommended Python Version: `>=3.9, <=3.11`

#### As a python library
`pip install -i https://test.pypi.org/simple/ shark-atplab==1.0.0.dev0`

** This allows users to import functionalities as python package  

#### As a cmd utility
`git clone https://git.mpi-cbg.de/tothpetroczylab/shark.git`

** Only this allows user to run the functionalities as a command line utility 

Install dependencies: `pip install -r requirements.txt`


###  How to use
________________
### 1. Dive

#### 1.1. Scoring: Given two protein sequences and a k-mer length (1 to 20), score the similarity b/w them 

##### Inputs

1. Protein Sequence 1
2. Protein Sequence 2
3. Scoring-variant: Normal (`SHARK-score (T)`)/ Sparse (`SHARK-score (best)`)
   1. Threshold (for "Normal")
4. K-Mer Length (Should be <= smallest_len(sequences))

##### 1.1.1. As a command-line utility
- Run the python script `src/shark_atplab/dive/run.py`
- Enter sequences when command prompts
- Enter the variant (1/2) when the command prompts
```
% python src/shark_atplab/dive/run.py 
Enter Sequence 1:
> SSSSPINTHGVSTTVPSSNNTIIPSSDGVSLSQTDYFDTVHNRQSPSRRESPVTVFRQPSLSHSKSLHKDSKNKVPQISTNQSHPSAVSTANTPGPSPN
Enter Sequence 2:
> VAEREFNGRSNSLHANFTSPVPRTVLDHHRHELTFCNPNNTTGFKTITPSPPTQHQSILPTAVDNVPRSKSVSSLPVSGFPPLIVKQQQQQQLNSSSSASALPSIHSPLTNEH
Enter k-mer length (integer 1 - 10): > 5
Press: 1. Normal; 2. Sparse
> 1
Enter threshold:
>0.8
Similarity Score: 0.6552442773
```

##### 1.1.2. As an imported python package
```
from shark_atplab.core import utils
from shark_atplab.dive.run import run_normal, run_sparse

dive_t_score = run_normal(
    sequence1="LASIDPTFKAN",
    sequence2="ERQKNGGKSDSDDDEPAAKKKVEYPIAAAPPMMMP",
    k=3,
    threshold=0.8
)   # Compute SHARK-score (T)  

dive_best_score = run_sparse(
    sequence1="LASIDPTFKAN",
    sequence2="ERQKNGGKSDSDDDEPAAKKKVEYPIAAAPPMMMP",
    k=3,
)   # Compute SHARK-score (best)

```

#### 1.2. Similarity Prediction

##### 1.2.1. As an imported python package
```
from shark_atplab.dive.prediction import Prediction

predictor = Prediction(q_sequence_id_map=<dict-fasta-id-seq>, t_sequence_id_map=<dict-fasta-id-seq>)

expected_out_keys = ['seq_id1', 'sequence1', 'seq_id2', 'sequence2', 'similarity_scores_k', 'pred_label', 'pred_proba']
output = predictor.predict()    # List of output objects; Each element is for one pair
```

##### 1.2.2. As a command-line utility
- Run the python script `src/shark_atplab/dive/prediction.py` with the absolute path of the sequence fasta file as only argument
- Sequences should be of length > 10, since `prediction` is always based on scores of k = [1..10]


_You may use the `sample_fasta_file.fasta` from `data` folder (Owncloud link)_

```
% python dive/prediction.py "<query-fasta-file>.fasta" "<target-fasta-file>.fasta"
Read fasta file from path <query-fasta-file>.fasta; Found 4 sequences; Skipped 0 sequences for having X
Read fasta file from path <target-fasta-file>.fasta; Found 6 sequences; Skipped 0 sequences for having X
Output stored at <DATA_DIR>/<path-to-sequence-fasta-file>.fasta.csv
```
- Output CSV has the following column headers: 
    - (1) "Query": Fasta ID of sequence from Query list
    - (2) "Target": Fasta ID of sequence from Target list
    - (3..12) "SHARK-Score (k=*)": Similarity score between the two sequences for specific k-value
    - (13) "SHARK-Dive": Aggregated similarity score over all lengths of k-mer

_________

## Developer section

The following directory structure allows a developer to understand the codebase 

### Directory Structure
________________________
```
|-- shark_atplab                # Package root
    |-- core                    # Core logic of sequence similarity matrix and common utilities
    |-- dive                    # Source code/logic functions related to "Dive"
|-- data                        # Local folder: Data directory
|-- tests                       # Unit tests
|-- requirements.txt            # Packages required for the project
|-- README.md

```

#### Simply run all unit-tests
`python3 -m unittest`

Generate coverage:

```
coverage run -m unittest
coverage report 
```


#### Packaging and PyPI

For now, we are uploading it only to testpypi
https://test.pypi.org/project/shark-atplab/

1. `python3 -m pip install --upgrade build`
2. `python3 -m build`
3. `python3 -m pip install --upgrade twine`
4. `python3 -m twine upload --repository testpypi dist/*`

__________

## Publication
### SHARK enables homology assessment in unalignable and disordered sequences
`Chi Fung Willis Chow, Soumyadeep Ghosh, Anna Hadarovich, Agnes Toth-Petroczy*`

_Under review_

Biorxiv link: https://www.biorxiv.org/content/10.1101/2023.06.26.546490v1

_________
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
