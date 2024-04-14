# pollychem/featurize.py

"""
Desc: Transform chemical structures or smiles strings to numeric vectors for ML input.
"""

import numpy as np
from molfeat.trans.fp import FPVecTransformer
from molfeat.trans import MoleculeTransformer
import torch
from transformers import AutoModelWithLMHead, AutoTokenizer
from .maplight import get_fingerprints

import warnings, logging
warnings.filterwarnings("ignore")

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import numpy as np


class SmilesFeaturizer:
    """Define featurizer class.

    Example:
    >>> featurizer = SmilesFeaturizer(feature_type='desc2D')
    """

    def __init__(self, feature_type='desc2D', kwargs={}):
        """Initialize featurizer object with passed option.

        Params
        ------
        feature_type : str or python func
            Featurizer option. Pass a string (one of the fingerprints in molfeat library)
            or a custom function which transforms a smiles string to a numpy 1-d vector.
            Default is 'desc2D'.
        kwargs : Dict (optional)
            Dictionary of parameters to be passed to custom featurizer function. Default : {}

        Returns
        -------
        None:
            feature_type attribute is update to hold the selected option and any tunable parameters.
        """

        self.feature_type = feature_type
        self.featurizer_args = kwargs

    def transform(self, dataset, smiles_col='Drug'):
        """Transform a list of smiles strings to a numeric feature array.

        Params
        ------
        dataset : pd.DataFrame
            Table containing compounds list to be featurized.
        smiles_col : str (optional)
            Table column containing the smiles list. Default : 'Drug'

        Returns
        -------
        np.array : Numpy matrix of size N x D, where N = no. of input smiles and D = dimensionality of feature vector.
        """

        logging.info(f"Featurizing molecules using {self.feature_type} option...")
        smiles = dataset[smiles_col]
        # Sanitize and standardize your molecules if needed
        try:
            
            if isinstance(self.feature_type, str):

                if self.feature_type == 'maplight':
                    # From https://github.com/maplightrx/MapLight-TDC/blob/main/maplight.py
                    feature_mat = get_fingerprints(smiles)

                elif self.feature_type in ['desc2D', 'ecfp', 'fcfp', 'maccs', 'avalon', 'rdkit']: 
                    mol_transf = FPVecTransformer(kind=self.feature_type, dtype=np.float32, n_jobs=-1)  # fingerprints
                    feature_mat = mol_transf(smiles)

                elif self.feature_type in ['mordred']:  
                    mol_transf = MoleculeTransformer(featurizer=self.feature_type, dtype=float, n_jobs=-1)  # chem-phys descriptors
                    feature_mat = mol_transf(smiles)

                elif self.feature_type == 'ChemBERTa_zinc_base_v1':
                    # https://huggingface.co/seyonec/ChemBERTa-zinc-base-v1, 
                    # https://github.com/seyonechithrananda/bert-loves-chemistry/tree/master
                    model = AutoModelWithLMHead.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")
                    tokenizer = AutoTokenizer.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")
                    # Embeddings are averaged across all tokens per smiles, ignoring 1st and last tokens which are fixed
                    outputs = [torch.mean(model(tokenizer.encode(s, return_tensors="pt")).logits[:,1:-1,:], dim=1).detach().numpy() for s in smiles]
                    feature_mat = np.vstack(outputs)

            else:

                # Use custom feature fn, passing necessary arguments
                feature_mat = np.stack(smiles.apply(self.feature_type, **self.featurizer_args))

            logging.info(f"Feature matrix has shape : {feature_mat.shape}")
            return feature_mat

        except Exception as e:
            logging.error(f'Error featurizing input smiles list: {str(e)}') 


"""
Desc: Class for converting SMILES into molecular feature vectors.
"""

class MolecularFeaturizer:
    """
    Class to handle the conversion of SMILES strings into molecular feature vectors.
    """

    def __init__(self, n_bits=1024, radius=2, use_features=True):
        """
        Initializes the MolecularFeaturizer with default parameters for the feature vector.

        Parameters:
        n_bits (int): Number of bits in the feature vector. Default is 1024.
        radius (int): Radius of the Morgan algorithm. Default is 2.
        use_features (bool): Whether to use feature-based Morgan fingerprints. Default is True.
        """
        self.n_bits = n_bits
        self.radius = radius
        self.use_features = use_features

    def custom_featurizer(self, smiles):
        """
        Converts a SMILES string into a feature vector using the Morgan fingerprint algorithm.

        Parameters:
        smiles (str): The SMILES string of the molecule.

        Returns:
        np.array: Numpy array representing the feature vector of the molecule.
        """
        mol = Chem.MolFromSmiles(smiles)  # Convert SMILES to RDKit Mol object
        if not mol:
            raise ValueError("Invalid SMILES string provided.")

        fp_vec = rdMolDescriptors.GetMorganFingerprintAsBitVect(
            mol,
            radius=self.radius,
            nBits=self.n_bits,
            useFeatures=self.use_features
        )
        # Convert the bit vector to a numpy array
        fp = np.frombuffer(fp_vec.ToBitString().encode(), 'u1') - ord('0')
        return fp