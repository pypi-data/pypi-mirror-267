# pollychem/model.py

"""
Desc: Model class and methods to train, tune, and test/predict with ML models fitted to cheminformatics data.
"""

import numpy as np
import pandas as pd
import logging
from functools import partial
import tempfile
from pathlib import Path

import splito

from sklearn.linear_model import LogisticRegression, ElasticNet
from sklearn.model_selection import train_test_split, ParameterGrid

from skopt import gp_minimize, dummy_minimize

from .utils import MetricsEvaluator

import mlflow
from mlflow.models import infer_signature

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers



class DataSplitter:
    """
    Handles splitting of datasets into training, validation, and testing sets using various strategies.
    """
    
    def __init__(self, split_type='scaffold', test_size=0.2, val_size=None, random_seed=42):
        """
        Initializes the DataSplitter with default splitting parameters.

        Parameters:
        split_type (str): The method used for splitting the dataset. Options: 'scaffold', 'perimeter', 'random', 'stratified'.
        test_size (float): The proportion of the dataset to include in the test split.
        val_size (float, optional): The proportion of the training dataset to include in the validation split.
        random_seed (int): The random seed for reproducibility.
        """
        self.split_type = split_type
        self.test_size = test_size
        self.val_size = val_size
        self.random_seed = random_seed

    def split_data(self, dataset, smiles_col='Drug',label_col='Y'):
        """Wrapper around splito/sklearn to split list of smiles strings into train & test sets.

        Params
        ------
        dataset : pd.DataFrame
            Input data table containing compounds and property values.
        smiles_col : str (optional)
            Table column containing the smiles list. Default : 'Drug'
        label_col : str (optional)
            Table column to be used as the target variable. Default : 'Y'

        Returns
        -------
        np.array : 1-d array of indices corresponding to train set
        np.array : 1-d array of indices corresponding to test set

        Raises
        ------
        ValueError : If input split_type is unrecognized.
        """
        
        logging.info(f"Splitting dataset for training using {self.split_type} split...")

        if self.split_type == 'scaffold':
            splitter = splito.ScaffoldSplit(smiles=dataset[smiles_col].values, 
                                                n_jobs=-1, test_size=self.test_size, random_state=self.random_seed)
            train_idx, test_idx = next(splitter.split(X=dataset[smiles_col].values))
            assert train_idx.shape[0] > test_idx.shape[0]

        elif self.split_type == 'perimeter':
            splitter = splito.PerimeterSplit(smiles=dataset[smiles_col].values, 
                                                n_jobs=-1, test_size=self.test_size, random_state=self.random_seed)    
            train_idx, test_idx = next(splitter.split(X=dataset[smiles_col].values))
            assert train_idx.shape[0] > test_idx.shape[0]

        elif self.split_type == 'stratified':
            y = dataset[label_col]
            train, test = train_test_split(y, test_size=self.test_size, stratify=y, random_state=self.random_seed)
            train_idx = np.where(y.index.isin(train.index))[0]
            test_idx = np.where(y.index.isin(test.index))[0]

        elif self.split_type == 'random':
            np.random.seed(self.random_seed)
            dataset_size = dataset.shape[0]
            train_idx = np.random.randint(0, dataset_size, size=int((1-self.test_size)*dataset_size))
            test_idx = np.setdiff1d(range(dataset_size), train_idx)

        else:
            logging.error(f"Split type {self.split_type} unrecognized.")
            raise ValueError("Split type not recognized; choose one of 'scaffold', 'stratified' or 'random'.")
        
        return train_idx, test_idx


    def create_training_data(self, dataset, X,
                            label = 'Y',
                            smiles_col = 'Drug'):
        """Split labeled assay data into train/eval/test sets for ML training. 
        
        Params
        ------
        dataset : pd.DataFrame
            Input data table containing compounds and property values.
        label : str (optional)
            Table column to be used as the target variable. Default : 'Y'
        split_type : str (optional)
            Logic for dataset splitting. Current options are 'scaffold', 'perimeter', 'random' and 'stratified'.
            Default : 'scaffold'.
        smiles_col : str (optional)
            Table column containing the smiles list. Default : 'Drug'
        test_size : float (optional)
            Fraction of data to assign to holdout test set. Default : 0.2
        val_size : float>0 or None (optional)
            Fraction of the train data created to be used for cross-validation.
            Default : None (no separate eval set created)    
        
        Returns
        -------
        tuple (np.array, pd.Series) : Feature matrix and labels for the training set
        tuple (np.array, pd.Series) : Feature matrix and labels for the eval set
        tuple (np.array, pd.Series) : Feature matrix and labels for the hold-out test set
        """
        
        train_idx, test_idx = self.split_data(dataset, smiles_col=smiles_col, label_col=label)
        if isinstance(self.val_size, float):
            # Split the train set further into train and val sets if val_size is not None; this overwrites the above train_idx list
            dev_set = dataset.iloc[train_idx].copy()
            train_idx, val_idx = self.split_data(dev_set, smiles_col=smiles_col, label_col=label)

        # Column in input data to be treated as target
        if label is None:
            label_column = [c for c in dataset.columns if 'drug' not in c.lower()][0]  # default option
        else:
            label_column = label
        y = dataset[label_column]  # Property table

        # Create X,y pairs for train/val/test
        X_train, X_test = X[train_idx,:], X[test_idx,:]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        if 'val_idx' in locals():
            X_val, y_val = X[val_idx,:], y.iloc[val_idx]
        else:
            X_val, y_val = None, None

        if X_val is None:
            logging.info(f"Created train/test splits with sizes : {X_train.shape} / {X_test.shape}")
        else:
            logging.info(f"Created train/eval/test splits with sizes : {X_train.shape} / {X_val.shape} / {X_test.shape}")

        return (X_train, y_train), (X_val, y_val), (X_test, y_test)


class PropertyPredictionModel:
    """Class for creating, training and/or tuning property prediction models and logging expts."""

    def __init__(self, train=None, model_type='classifier', model_id='lr_classifier', model_params={}):
        """Initialize model object.

        Example:
        >>> lr_params = {'penalty':'l2', 'C':1.0, 'fit_intercept':True}
        >>> model = ProprtyPredictionModel(model_type='classifier', model_id='lr_classifier', model_params=lr_params)

        Params
        ------
        train : (np.array, pd.Series)
            Train feature matrix and labels. This is needed, e.g. if the input size has to be inferred when creating
            a Keras NN. Default : None
        model_type : str
            Type of model: 'classifier' or 'regressor'. Default : 'classifier'
        model_id : str or model class from sklearn models or python func
            Model to be initialized. Default options are 'lr_clasifier' or 'elastic_regressor'.
            Can provide any ML model object class with fit, predict, get_params and set_params methods.
            E.g. (sklearn) : LogisticRegression, SVC
            Also can provide a custom model (e.g. a Keras NN) defined through a python function.
            Default : 'lr_classifier'
        model_params : Dict
            Key:Value dict supplying any model/training params. Default : {}
                    
        Returns
        -------
        None : Model object is initialized with attributes model_type, model_id, model, params, metrics and history.         
        """
        
        self.model_type = model_type  # classifier or regressor
        self.model_id = model_id  # This will be used inside the tune function to initialize models
        
        if isinstance(model_id, str):
            if model_id == 'lr_classifier':
                set_params = {**{'solver':'liblinear', 'class_weight':'balanced'}, **model_params}
                self.model = LogisticRegression(**set_params)
                self.params = set_params
            elif model_id == 'elastic_regressor':
                self.model = ElasticNet(**model_params)
                self.params = model_params
            else:
                raise ValueError(f"{model_id} is not a valid model id.")
        else:
            if hasattr(model_id, 'get_params'):
                # This option is for model objs with get_params/set_params methods
                self.model = model_id()
                valid_params = list(self.model.get_params().keys())
                # Pass only the valid model params in the input dict to avoid error
                set_params = {k:v for k,v in model_params.items() if k in valid_params}
                self.model.set_params(**set_params)
                self.params = set_params
            else:
                # Option for custom-defined models
                set_params = {**{'train':train}, **model_params}
                self.model = model_id(**set_params)
                self.params = model_params
        
        self.metrics = None
        self.history = None
        
        logging.info(f"Initialized model : {model_id}.")

    def train(self, train, test=None, log_run=False, run_name=None, run_desc=''):
        """Train model, return eval metrics on test set (if supplied).
        
        Params
        ------
        train : (np.array, pd.Series)
            Training feature matrix and labels
        test : (np.array, pd.Series) [optional]
            Test feature matrix and labels, if model is to evaluated on hold-out data. Default : None
        log_run : Bool (optional)
            Whether to log training run to tracking server (using Mlflow as an example here). Default : False
        run_name : str (optional)
            If logging expt, name to be assigned to current run. Default : None
        run_desc : str (optional)
            Any optional description to add when logging current run. Default : ''

        Returns
        -------
        Dict : Prediction metrics for the trained model, evaluated on the hold-out test set, as key:value pairs.
        None : Model object is update in-place by updating model, history and metrics attributes.
        """

        X_train, y_train = train
        if hasattr(self.model, '__module__'):
            if self.model.__module__.startswith('tensorflow') or self.model.__module__.startswith('keras'):
                history = self.model.fit(X_train,
                                    y_train,
                                    batch_size=self.params.get('batch_size', 64),
                                    validation_split=0.1,
                                    verbose=0, 
                                    epochs=self.params.get('epochs', 20))
                self.history = history.history
            elif self.model.__module__.startswith('torch'):
                print("It's a Pytorch model")
                # TBD - Add code to handle pytorch models
            else:  
                #if self.model.__module__.startswith('sklearn'):
                self.model.fit(X_train, y_train)
            logging.info(f"Trained model with params : {self.params}")
            
            # Test the fitted model on hold-out test set:
            if test is not None:
                test_metrics = self.evaluate(test)
            else:
                test_metrics = {}
        
        else:
            
            logging.error("Model object is unrecognized; cannot run training step.")
            test_metrics = {}

        self.metrics = test_metrics   # Save test metrics as instance attribute

        # Log expt run to mlflow
        if log_run:
            try:
                with mlflow.start_run(run_name = run_name, description=run_desc):
                    run_id = mlflow.active_run().info.run_id
                    mlflow.set_tag('Training run', f'Single run for model : {self.model_id}')
                    mlflow.log_params(self.params)
                    mlflow.log_metrics(test_metrics)
                    
                    io_temp = [X_train[0:1], self.model.predict(X_train[0:1])]
                    signature = infer_signature(io_temp[0], io_temp[1])
                    if hasattr(self.model, '__module__'):
                        model_lib = self.model.__module__.split('.')[0]
                        log_model(self.model, model_type=model_lib, signature=signature)
                    
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        path = Path(tmp_dir, "train.csv")
                        pd.concat([pd.DataFrame(train[0]), train[1]],axis=1).to_csv(path, sep='\t')
                        path = Path(tmp_dir, "test.csv")
                        pd.concat([pd.DataFrame(test[0]), test[1]],axis=1).to_csv(path, sep='\t')
                        mlflow.log_artifacts(tmp_dir, artifact_path="datasets")
                logging.info(f"Logged run {run_id} to tracking server.")
            except Exception as e:
                logging.error(f"Error logging run : {str(e)}")

        return test_metrics
        
    def predict(self, X_test):
        """Predict property labels/values of a set of compounds.
        
        Params
        ------
        X_test : np.array
            Feature matrix of the input compounds. Should use the same features that the model was trained on.

        Returns
        -------
        pd.Series : Predictions (binary/float) for the input set. 
        """

        if hasattr(self.model, 'predict'):
            y_pred = self.model.predict(X_test)
            if self.model_type == 'classifier':
                y_pred = (y_pred > 0.5).astype(int)
            return y_pred
        else:
            logging.error("Model does not have 'predict' method.")
            # TBD - Add code to handle pytorch models
            return None
        
    def evaluate(self, test):
        """Evaluated trained model on a hold-out test set.
        
        Params
        ------
        test : (np.array, pd.Series)
            Feature matrix and labels of the compounds in the test set.

        Returns
        -------
        Dict : Eval metrics as key:value pairs. 
        """
        
        evaluator = MetricsEvaluator()

        y_pred = self.predict(test[0])
        y_test = test[1]
            
        if self.model_type == 'classifier':
            test_metrics = evaluator.eval_classifier_metrics(y_pred, y_test)
        else:
            test_metrics = evaluator.eval_regressor_metrics(y_pred, y_test)
            
        logging.info(f"Test metrics : {test_metrics}")
        return test_metrics
        
    def tune(self, train, eval, test, param_grid, sampling='all', scoring_metric='balanced_accuracy', n_samples=10, log_run=False):
        """Loop over different hypaerparameter combinations, train/eval model for each combination, 
           and return the optimal set of params (giving best eval score). Uses scikit-optimize library.

        Params
        ------
        train : (np.array, pd.Series)
            Feature matrix and labels of the training set
        eval : (np.array, pd.Series)
            Feature matrix and labels of the eval set (to be used for validation)
        test : (np.array, pd.Series)
            Feature matrix and labels of the hold-out test set (for reporting the metrics of the final tuned model)
        param_grid : Dict
            Dict of key:value pairs specifying the ranges of the parameters to be varied during model tuning.
            This can be supplied in a separate params.py file (see params.py for examples)
        sampling : str
            How the hyperparams are to be sampled during model tuning. Options are:
            Grid-based : 'all' (exhaustive)
            Distribution-based: 'random' (random) and 'gp' (gaussian-process); these are sampling options in sk-optimize.
        scoring_metric : str
            Eval metric to be used to rate and compare models (param sets) on the eval data.
            Default (for classifier) : 'balanced_accuracy'
        n_samples : int
            No. of param combinations to be sampled (relevant for random and gp sampling options). Default : 10
        log_run : Bool (optional)
            Whether to log training runs to tracking server (using Mlflow as an example here). Default : False

        Returns
        ------- 
        List : Sequence of scores of all the models (tested param combinations). 
                When sk-optimize is used, additional metrics and details are included in the output.
        None : Model instance is updated in-place, with model holding the best model (trained on train + eval using the best params),
                metrics holding the metrics evaluated on hold-out test set, and params holding the best params set.
        """

        logging.info(f"Tuning model hyperparameters using sampling : {sampling}")

        if sampling == 'all':
            runs = 0
            res = []
            best_score = float('-inf') if scoring_metric not in ['RMSE', 'MAE'] else float('inf')
            best_params = None
            logging.info(f"Param grid : {param_grid}")
            for params in ParameterGrid(param_grid):
                runs += 1
                model = PropertyPredictionModel(train=train,
                                                model_type=self.model_type, 
                                                model_id=self.model_id, 
                                                model_params={**self.params, **params}) 
                eval_metrics = model.train(train, eval, log_run=log_run)
                res.append(eval_metrics[scoring_metric])
                if scoring_metric not in ['RMSE', 'MAE']:
                    if eval_metrics[scoring_metric] > best_score:
                        best_score = eval_metrics[scoring_metric]
                        best_params = params
                else:
                    if eval_metrics[scoring_metric] < best_score:
                        best_score = eval_metrics[scoring_metric]
                        best_params = params

            logging.info(f"Completed {runs} hyperparameter runs.")

        else:

            logging.info(f"Param ranges : {param_grid}")
            def func(param_values, param_keys):
                params = dict(zip(param_keys, param_values))
                model = PropertyPredictionModel(train=train,
                                                model_type=self.model_type, 
                                                model_id=self.model_id,  
                                                model_params={**self.params, **params})
                eval_metrics = model.train(train, eval, log_run=log_run)
                score = eval_metrics[scoring_metric] if scoring_metric not in ['RMSE','MAE'] else 1 - eval_metrics[scoring_metric]
                return score
            # Create a dummy function with list argument for compatibility with skopt
            f = partial(func, param_keys=list(param_grid.keys())) 
            space = list(param_grid.values())
            if sampling=='gp':
                # Sequential sampling
                res = gp_minimize(f,
                                space,
                                acq_func="EI",
                                n_calls=n_samples-5,
                                n_initial_points=5,
                                n_points=1000,
                                noise=0,
                                random_state=42
                                )
            else:
                # Random sampling
                res = dummy_minimize(f,
                                space,
                                n_calls=n_samples,
                                random_state=42
                                )
            logging.info(f"Completed {n_samples} iterations.")
            best_params = dict(zip(list(param_grid.keys()), res.x))

        logging.info(f"Best params : {best_params}")
        logging.info(f"Fitting final model to the combined train + eval set...")
        # Fit model to the combined train + eval set using the best-scoring params, this will be available in self.model
        train_all = np.vstack((train[0], eval[0])), pd.concat([train[1], eval[1]], axis=0)
        model = PropertyPredictionModel(train=train_all,
                                        model_type=self.model_type, 
                                        model_id=self.model_id,  
                                        model_params={**self.params, **best_params})
        _ = model.train(train_all, test, 
                            log_run=log_run, 
                            run_name='Best_Model',
                            run_desc = 'Final model trained on train + eval set using best params.')
        self.model = model.model
        self.params = model.params
        self.metrics = model.metrics

        return res 

def keras_nn_classifier(**kwargs):
    
    train = kwargs.get('train')  # Need this to initialize the normalization layer
    n_layers = kwargs.get('n_layers', 1)  # Num of hidden layers
    hidden_dim = kwargs.get('hidden_dim', 64)  # Fixed num units per hidden layer
    lr = kwargs.get('lr', 0.001)  # Learning rate
    
    model = keras.Sequential()
    # Scale features before passing to NN (using the train set)
    normalizer = layers.Normalization(axis=-1)
    normalizer.adapt(train[0])
    model.add(normalizer)
    # Add hidden layers
    for _ in range(n_layers):
        model.add(layers.Dense(hidden_dim, activation='relu'))
    # Add single output unit
    model.add(layers.Dense(1, activation='sigmoid'))
    
    # Compile model
    model.compile(loss='binary_crossentropy',
                optimizer=keras.optimizers.Adam(learning_rate=lr),
                metrics=['accuracy'])
    
    return model


def log_model(model, model_type='sklearn', signature=None):
    """
    Logs a model to MLflow.
    Parameters:
    model (model object): The machine learning model to log.
    model_type (str): The type of the model ('sklearn', 'keras', etc.).
    signature (mlflow.models.Signature, optional): The model signature for MLflow to understand the input and output formats.

    Returns:
    None
    """
    if model_type == 'sklearn':
        mlflow.sklearn.log_model(model, 'model', signature=signature)
    elif model_type == 'keras':
        mlflow.keras.log_model(model, 'model', signature=signature)
    else:
        logging.error(f"Unsupported model type: {model_type}")
        raise ValueError(f"Unsupported model type: {model_type}")