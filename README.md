# Yelp Dataset Analysis: Gender Prediction

Implementation and evaluation of an SVM classifier to predict the gender of a user based
on her written reviews.

*Remark*: The pipeline computes estimators for six different settings, which could take
some time to compute. My results were reached with datasets of size 80,000 users and a 
maximum feature size of 10,000 features, but much smaller training parameters yield
almost the same accuracies:

- *Params 1:* 80,000 samples (users), 10,000 Features
- *Params 2:* 10,000 samples (users), 1,000 Features

Reviews / User | Params 1 | Params 2
---------------|----------|---------
 1   | 0.70 | 0.67
 2   | 0.76 | 0.73
 5   | 0.84 | 0.79
 10  | 0.89 | 0.86
 20  | 0.91 | 0.88
 all | 0.75 | 0.73


## Running inside Docker Container
1. Download the [Yelp Dataset](https://www.yelp.com/dataset/download) and extract it to
   `<project_dir>/data/yelp_dataset`:
   ```
   mkdir <project_dir>/data/yelp_dataset
   tar zxvf yelp_dataset.tgz -C <project_dir>/data/yelp_dataset  
   ```

1. Download and run `jupyter/scipy-notebook` Docker stack **from inside the project 
   root directory**:
   ```
   docker run --rm -p 8888:8888 -v "$PWD":/home/jovyan/work \
   jupyter/scipy-notebook:016833b15ceb
   ```
   *Remark*: Ensure that the Docker container has permissions to bind to the project
   directory.

1. Open the displayed link in your browser:
   ```
   http://127.0.0.1:8888/?token=<token is shown in terminal>
   ```
   
 1. The notebooks are located inside the `work` directory
    - Open and execute `data_preparation.ipynb` to prepare the training and test data
    - Open and execute `train_estimators.ipynb` to train the estimators
    - Open and execute `estimator_evaluation.ipynb` to compute accuracy on test datasets

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
- **Hyperparameter optimization**: Run an extensive grid search on the created datasets 
  (truncated to 20000 samples each). The best parameters are outputted to stdout.
  ```
  python3 main_parameter_optimization.py
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
  jupyter notebook estimator_evaluation.ipynb  
  ```

## SQLite database
The CLI tool `main_create_sqlite_database.py` creates an SQLite database from the Yelp
dataset JSON files. This database is not required for the data analysis, but can be used
for an initial data exploration.

*Remark*: The `--language` option works only if pyCLD3 is installed
(`pip install pycld3`), which is not listed as a requirement.

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