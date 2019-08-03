# Install

1. Download openbabel https://sourceforge.net/projects/openbabel/files/openbabel/2.4.1/openbabel-2.4.1.tar.gz/download
2. Install openbabel
  ```
  tar zxf openbabel-2.4.1.tar.gz
  mkdir build
  cd build
  cmake ../openbabel-2.4.1 -DPYTHON_BINDINGS=ON -DPYTHON_EXECUTABLE=/usr/local/bin/python3 -DRUN_SWIG=ON
  make -j4
  make install
  ```
3. Create virtual environment & install dependencies
  ```
    # In phytebyte root directory
    python3 -m venv env
    pip install -r requirements.txt
  ``` 
4. Install pybel (Python wrapper for openbabel)
  ```
    pip install openbabel
  ```
5. Download the 'FooDB SQL file' from [http://foodb.ca/downloads](http://foodb.ca/downloads) 
6. Unzip the file
```
gunzip foodb_2017_06_29.sql.gz
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
cat foodb_2017_06_29.sql | mysql -uroot -pphytebyte foodb
``` 
8. Install postgresql
```
brew install postgres
brew services start postgres
# Verify you can connect
psql  # Should open `psql>` prompt
# Create the 'chembl' database
CREATE DATABASE chembl_25;
```
8. Download & decompress ChEMBL Database (for postgresql)
```
curl -O http://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_25/chembl_25_postgresql.tar.gz
gunzip chembl_25_postgresql.tar.gz
tar xopf chembl_25_postgresql.tar
cd chembl_25/chembl_25_postgresql
pg_restore -d chembl_25 chembl_25_postgresql.dmp
```
9. Set ENV variables in ~/.bash_profile
```
# Open up ~/.bash_profile with text-editor, enter following at bottom
export FOODB_URL="mysql://root:phytebyte@localhost/foo_db"
export CHEMBL_DB_URL="postgres:///chembl_25"
```
10. Re-load ~/.bash_profile
```
source ~/.bash_profile
```
11. Run Tests
```
# From phytebyte root dir
pytest -vv tests
```

12. Run Phytebyte!

