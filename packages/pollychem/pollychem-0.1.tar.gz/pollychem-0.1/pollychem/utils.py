# pollychem/utils.py

"""
Desc: Additional helper functions for evaluation metrics and data visualization.
"""

import numpy as np
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    accuracy_score, balanced_accuracy_score, f1_score
)

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('darkgrid')

class MetricsEvaluator:
    """Class to evaluate performance metrics for classification and regression models."""

    @staticmethod
    def eval_classifier_metrics(y_pred, y_true):
        """
        Calculate various classification metrics.

        Parameters:
        y_pred (array-like): Predicted labels.
        y_true (array-like): True labels.

        Returns:
        dict: Dictionary of classification metrics including accuracy, balanced accuracy, and F1 score.
        """
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
            "f1_score": f1_score(y_true, y_pred, average='macro')
        }
        return metrics

    @staticmethod
    def eval_regressor_metrics(y_pred, y_true):
        """
        Calculate various regression metrics.

        Parameters:
        y_pred (array-like): Predicted values.
        y_true (array-like): True values.

        Returns:
        dict: Dictionary of regression metrics including RMSE, MAE, and R2.
        """
        metrics = {
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "MAE": mean_absolute_error(y_true, y_pred),
            "R2": r2_score(y_true, y_pred)
        }
        return metrics

class DataVisualizer:
    """Class to handle data visualization tasks."""

    @staticmethod
    def plot_property_distribution(dataset, label_col='Y'):
        """
        Plot the frequency distribution of a property in the dataset.

        Parameters:
        dataset (pd.DataFrame): Dataset containing the property.
        label_col (str): Column name of the property to be visualized.

        Returns:
        None: Displays a histogram or bar plot depending on the property type.
        """
        plt.figure(figsize=(10, 6))
        if len(set(dataset[label_col])) < 10:
            dataset[label_col].value_counts().sort_values().plot(kind='barh')
        else:
            sns.histplot(data=dataset, x=label_col, kde=True)
        plt.show()
