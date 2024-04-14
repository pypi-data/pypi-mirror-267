# pollychem/data.py

"""
Desc: Dataset loaders to fetch assay data from public DBs
"""

import pandas as pd
import math
import os
import urllib.request
import shutil
import zipfile
import gzip
import logging
from tqdm.auto import tqdm

from tdc.single_pred import ADME
from chembl_webresource_client.new_client import new_client

class DatasetLoader:
    """Class for loading datasets from public databases such as TDC, PubChem, and ChEMBL."""

    def __init__(self):
        self.pubchem_folder = "./pubchem_downloads"
        self.chembl_folder = "./chembl_downloads"
        os.makedirs(self.pubchem_folder, exist_ok=True)
        os.makedirs(self.chembl_folder, exist_ok=True)

    def load_tdc_dataset(self, assay_id: str = "BBB_Martins") -> pd.DataFrame:
        """Load a bundled dataset from TDC for single-molecule ADME properties.

        Parameters:
            assay_id (str): TDC ID of assay data to be fetched.

        Returns:
            pd.DataFrame: Table with compound names, smiles, and property values.

        Raises:
            ValueError: If assay_id is invalid.
        """
        logging.info(f"Loading {assay_id} dataset from TDC...")
        try:
            data = ADME(name=assay_id)
            df = data.get_data()
            df.drop_duplicates(subset=['Drug'], inplace=True)
            df.dropna(inplace=True)
            logging.info('Removed duplicate and nan entries.')
            logging.info(f"{assay_id} dataset has {df.shape[0]} unique compounds.")
            return df
        except ValueError as ve:
            logging.error(f"Error loading {assay_id} : {str(ve)}")
            raise

    def load_pubchem_dataset(self, assay_id: str = "AID1706") -> pd.DataFrame:
        """Load a PubChem Bioassay dataset as a table of compounds and property values, checking for a local copy before downloading.

        Parameters:
            assay_id (str): PubChem ID of assay data to be fetched.

        Returns:
            pd.DataFrame: Table with compound names, smiles, and property values.

        Raises:
            IOError: If assay_id is invalid or data cannot be processed.
        """
        logging.info(f"Loading {assay_id} dataset from PubChem...")
        csv_file_path = os.path.join(self.pubchem_folder, f"{assay_id}.csv")
        
        # Check if the local CSV file already exists
        if os.path.exists(csv_file_path):
            logging.info(f"Local file {csv_file_path} found; loading it...")
            return self._read_and_process_pubchem_csv(csv_file_path)

        # If not, proceed to download and extract
        min_aid = str(math.floor(int(assay_id) / 1000) * 1000 + 1)
        max_aid = str(int(min_aid) + 999)
        zip_id = '0' * (7 - len(min_aid)) + min_aid + '_' + '0' * (7 - len(max_aid)) + max_aid
        ftp_url = f"https://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/CSV/Data/{zip_id}.zip"
        local_zip_path = os.path.join(self.pubchem_folder, f"{zip_id}.zip")
        
        if not os.path.exists(local_zip_path):
            logging.info(f"Local zip file not found; downloading from {ftp_url}...")
            with urllib.request.urlopen(ftp_url) as response, open(local_zip_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

        try:
            temp_file = os.path.join(zip_id, f"{assay_id}.csv.gz")
            with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                zip_ref.extract(temp_file, path=self.pubchem_folder)

            gz_file_path = os.path.join(self.pubchem_folder, temp_file)
            with gzip.open(gz_file_path, 'rb') as gz_file, open(csv_file_path, 'wb') as out_file:
                shutil.copyfileobj(gz_file, out_file)

            shutil.rmtree(os.path.join(self.pubchem_folder, zip_id))  # Clean up the extracted directory
            return self._read_and_process_pubchem_csv(csv_file_path)

        except IOError as e:
            logging.error(f"Error handling the file operations: {str(e)}")
            raise

    def _read_and_process_pubchem_csv(self, file_path: str) -> pd.DataFrame:
        """Reads and processes the CSV file to prepare the data.

        Parameters:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Processed data frame.

        Raises:
            pd.errors.EmptyDataError: If the file is empty or can't be processed.
        """
        df = pd.read_csv(file_path, sep=',', dtype={'PUBCHEM_CID': 'string'})
        df.set_index('PUBCHEM_CID', inplace=True)
        df.drop_duplicates(subset=['PUBCHEM_EXT_DATASOURCE_SMILES'], inplace=True)
        df.drop(columns=['PUBCHEM_ACTIVITY_URL', 'PUBCHEM_ASSAYDATA_COMMENT', 'PUBCHEM_RESULT_TAG', 'PUBCHEM_SID'], inplace=True)
        df.dropna(inplace=True)
        logging.info(f"Processed dataset from {file_path} with {df.shape[0]} unique compounds.")
        return df


    def load_chembl_dataset(self, assay_id: str = "CHEMBL3301365") -> pd.DataFrame:
        """
        Load a ChEMBL bioactivity assay dataset as a table of compound ids and property values + units.
        It first checks if a local copy of the dataset exists before attempting to download from ChEMBL.

        Parameters:
            assay_id (str): ChEMBL ID of assay data to be fetched.

        Returns:
            pd.DataFrame: Table with compound names, smiles, and property values.

        Raises:
            IOError: If assay_id is invalid or data retrieval fails.
        """
        logging.info(f"Attempting to load {assay_id} dataset from ChEMBL...")
        local_file_path = os.path.join(self.chembl_folder, f"{assay_id}.tsv")
        
        # Check if the local file exists and load it if so
        if os.path.exists(local_file_path):
            logging.info(f"Local file {local_file_path} found; loading it...")
            return self._read_and_process_chembl_csv(local_file_path)

        # If the local file doesn't exist, download the data
        logging.info("Local file not found; downloading from ChEMBL...")
        return self._download_and_save_chembl_data(assay_id, local_file_path)

    def _download_and_save_chembl_data(self, assay_id, local_file_path):
        try:
            activity = new_client.activity
            result = activity.filter(assay_chembl_id=assay_id).only(
                "assay_description", "assay_type", "molecule_chembl_id", "type", 
                "standard_units", "standard_value", "target_chembl_id"
            )
            res_df = pd.DataFrame.from_dict(result)
            res_df = res_df.astype({'standard_value': 'float32'}).drop_duplicates('molecule_chembl_id', keep='first').dropna()

            logging.info("Fetching chemical structures for compounds...")
            compounds_api = new_client.molecule
            compounds_provider = compounds_api.filter(
                molecule_chembl_id__in=list(res_df["molecule_chembl_id"])
            ).only("molecule_chembl_id", "molecule_structures")
            
            compounds = list(tqdm(compounds_provider, desc="Downloading compound data"))
            compounds_df = pd.DataFrame.from_records(compounds)
            compounds_df.dropna(axis=0, how="any", inplace=True)
            compounds_df.drop_duplicates("molecule_chembl_id", keep='first', inplace=True)

            canonical_smiles = [c["molecule_structures"]["canonical_smiles"] for c in compounds if "canonical_smiles" in c["molecule_structures"]]
            compounds_df["smiles"] = canonical_smiles
            compounds_df.drop("molecule_structures", axis=1, inplace=True)
            compounds_df.dropna(axis=0, inplace=True)

            res_df = pd.merge(res_df, compounds_df, on="molecule_chembl_id")
            res_df.to_csv(local_file_path, sep='\t', index=False)
            logging.info(f"Dataset downloaded and saved to {local_file_path}.")
        except Exception as e:
            logging.error(f"Error downloading dataset from ChEMBL: {str(e)}")
            raise

        return self._read_and_process_chembl_csv(local_file_path)

    def _read_and_process_chembl_csv(self, file_path):
        """
        Reads and processes the ChEMBL CSV data file.

        Parameters:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Processed dataset.
        """
        assay_id = os.path.basename(file_path).replace('.tsv', '')

        res_df = pd.read_csv(file_path, sep='\t')
        logging.info(f"Assay description: {res_df.iloc[0].get('assay_description', 'N/A')}")
        logging.info(f"Assay type: {res_df.iloc[0].get('assay_type', 'N/A')}")
        logging.info(f"{assay_id} dataset has {res_df.shape[0]} unique compounds.")

        # Return only the necessary columns, ensuring they exist
        necessary_columns = ['smiles', 'type', 'standard_value', 'standard_units', 'target_chembl_id']
        # Filter out columns that are present in the DataFrame
        df = res_df[[col for col in necessary_columns if col in res_df.columns]]
        return df
