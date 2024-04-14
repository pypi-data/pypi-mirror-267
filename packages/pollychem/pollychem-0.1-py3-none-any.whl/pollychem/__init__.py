# pollychem/__init__.py

# Import modules to make them available directly from the package namespace
from .utils import MetricsEvaluator, DataVisualizer
from .dataset_loader import DatasetLoader
from .preprocess import ChemDataPreprocessor
from .featurize import SmilesFeaturizer, MolecularFeaturizer
from .model import DataSplitter, PropertyPredictionModel, keras_nn_classifier

# Define package-level variables/constants
VERSION = '1.0'
AUTHOR = ''
