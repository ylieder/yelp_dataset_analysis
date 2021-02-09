# Yelp Dataset Analysis: Gender Prediction

## Local Installation
1. Download the [Yelp Dataset](https://www.yelp.com/dataset/download) and extract it to
   `<project_dir>/data/yelp_dataset`:
   ```
   mkdir <project_dir>/data/yelp_dataset
   tar zxvf yelp_dataset.tgz -C <project_dir>/data/yelp_dataset  
   ```

1. Install required Python libraries:
   ```
   pip install -r requirements.txt
   ``` 

## Local Execution
- **Create Training and Test datasets**:
  Open the notebook `data_preparation.ipynb` and execute all cells. Possible parameters
  are described inside the notebook.
  ```
  jupyter notebook data_preparation.ipynb  
  ```
- **Train an estimator**: Run the python script `main_estimator_training.py` in order
  to train a gender estimator. The estimator is exported to `data/estimators/` 
  ```
  python3 main_train_estimator.py <n_reviews> [<max. features>]
  ```
  *Arguments*: Number of reviews per user (specifies dataset), optional maximum number 
  of features, extracted from training data
- **Compute and visualize accuracy of estimators**: Open the notebook 
  `estimator_comparison.ipynb` and execute the cells.
  ```
  jupyter notebook estimator_comparison.ipynb  
  ```

## SQLite database
The CLI tool `main_create_sqlite_database.py` creates an SQLite database from the Yelp
dataset JSON files. This database is not required for the data analysis, but can be used
for an initial data exploration.

*Remark*: The `--language` option is only available after installing pyCLD3
(`pip install pycld3`), which is not listed as an requirement.

```
$ python3 main_create_sqlite_database.py --help
usage: main_create_sqlite_database.py [-h] [--gender] [--language] [--json_dir JSON_DIR] database_path

Create SQLite database from Yelp dataset JSONs.

positional arguments:
  database_path        Path to sqlite database

optional arguments:
  -h, --help           show this help message and exit
  --gender, -g         Add gender information to users
  --language, -l       Add language information to reviews
  --json_dir JSON_DIR  Path to Yelp dataset JSON files
```