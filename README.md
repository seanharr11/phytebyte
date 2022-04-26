# About

Phytebyte is an extensible software framework used to train machine learning models to identify bioactive compounds found in *food*. The use case captured in 'run.py' is training models using known drug compounds that target a specific gene, and identifying plant compounds in FooDB that *may* behave similarly.

# Install

1. Download openbabel
  ```
   curl -L https://github.com/openbabel/openbabel/archive/refs/tags/openbabel-3-1-1.tar.gz --output openbabel-3-1-1.tar.gz
2. Install openbabel
  ```
  tar zxf openbabel-3-1-1.tar.gz
  mkdir build
  cd build
  cmake ../openbabel-openbabel-3-1-1 -DPYTHON_BINDINGS=ON -DPYTHON_EXECUTABLE=/usr/local/bin/python3 -DRUN_SWIG=ON
  make -j4
  make install
  ```
3. Create virtual environment & install dependencies
  ```
    # In phytebyte root directory
    /usr/local/bin/python3 -m venv env
    # ^ Needs to be the same as PYTHON_EXECUTABLE flag in installation flag in prev step
    source env/bin/activate
    pip install -r requirements.txt
  ``` 
4. Install pybel (Python wrapper for openbabel)
  ```
    pip install openbabel
  ```
5. Download the 'FooDB SQL file' from [http://foodb.ca/downloads](http://foodb.ca/downloads) 
  ```
  curl -L https://foodb.ca/public/system/downloads/foodb_2020_4_7_mysql.tar.gz --output foodb.tar.gz
  # Check the URL above, new version may be available!
  ```
6. Unzip the file
```
mkdir foodb
tar zxf foodb.tar.gz -C foodb
```
6. Install mysql
```
brew install mysql
brew tap homebrew/services
brew services start mysql
# Change local admin password to whatever you'd like.
mysqladmin -u root password 'phytebyte'
# Verify that you can connect
mysql -uroot -pphytebyte
# Create the foodb Database
CREATE DATABASE foodb;
```
7. Load foodb Database
```
cat foodb_*.sql | mysql -uroot -pphytebyte foo_db
# Using wildcard to catch future versions of foodb database
``` 

8. Install postgresql
```
brew install postgres
brew services start postgres
# Verify you can connect
psql  # Should open `psql>` prompt
# Create the 'chembl' database
CREATE DATABASE chembl_30;
```
8. Download & decompress ChEMBL Database (for postgresql)
```
curl -O https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_30_postgresql.tar.gz
gunzip chembl_30_postgresql.tar.gz
tar xopf chembl_30_postgresql.tar
cd chembl_30/chembl_30_postgresql
pg_restore -d chembl_30 chembl_30_postgresql.dmp
```
9. Set ENV variables in ~/.bash_profile
```
# Open up ~/.bash_profile with text-editor, enter following at bottom
export FOODB_URL="mysql://root:phytebyte@localhost/foo_db"
export CHEMBL_DB_URL="postgres:///chembl_30"
export PYTHONPATH=/usr/local/lib/python3.9/site-packages:$PYTHONPATH
# Replace "python3.9" with the version with bindings linked in step 2/3
```
10. Re-load ~/.bash_profile
```
source ~/.bash_profile
```
11. Run Tests
```
# From phytebyte root dir
source env/bin/activate  # Active python virtual env
pytest -vv tests
```

12. Run Phytebyte!
```
python run.py
```

# Customization

**BioactiveCompoundSource**
The `BioactiveCompoundSource` abstract method defines an interface for fetching compounds by gene target, by name and via exclusion (by checking SMILES for equality). It represents a data source of compounds that will be queried to train a `BinaryClassifierModel`.

**TargetInputs**
The `TargetInput` is a simple data structure that tells the `BioactiveCompoundSource` what method to use when fetching input data for the `BinaryClassifierModel`. One can leverage the `GeneTargetsInput` (as done in run.py) to train a model on all compounds that either `agonize` or `antagonize` the given gene, in this use case, `PPARG`. Alternatively, the `CompoundNamesTargetInput` can be used to give a list of compound names found in ChEMBL to manually select the compounds used to train the model.

**Fingerprinters**
The `FP_TYPE` variable can be set to either `daylight` or `spectrophore` in `run.py`. Alternative fingerprints can be created by implementing the Fingerprinter abstract base class.

**FoodCmpdSource**
The `FoodCmpdSource` abstract base class can be further implemented to support additional food database sources. Our case study uses FooDB, but we encourage extending to other sources!

**BinaryClassifierModel**
The `BinaryClassifierModel` abstract base class can be further implemented to support alternative binary classifiers (SVM, LogisticRegression, etc.). Our use case leverages sklearn's `Random Forest`, and we also provide support for the `TanimotoBinaryClassifier` that uses tanimoto index to classify compounds.

# Config

**Fingerprinters**
In `run.py`, `FP_TYPE` can be set to either `spectrophore` or `daylight`

**Database URLs**
In `run.py` we use environment variables storing `CHEMBL_DB_URL` and `FOODB_URL`. These get passed to each respective `Source` for querying compounds.

**Negative Sample Size Factor**
The `neg_sample_size_factor` indicates the multiple applied to the number of `positive` compound samples (i.e. `20` means "20 times the number of positive samples").
