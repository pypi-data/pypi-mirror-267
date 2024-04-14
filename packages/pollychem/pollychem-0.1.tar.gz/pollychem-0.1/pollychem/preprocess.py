# pollychem/preprocess.py

"""
Desc: Helper functions to prep chem data for ML modeling.
"""

import medchem as mc
import datamol as dm
import pandas as pd
import logging

class ChemDataPreprocessor:
    """Class to handle the preprocessing of chemical data using medicinal chemistry filters."""

    def __init__(self, smiles_col="Drug", filters=['rule_of_five', 'PAINS']):
        """
        Initializes the ChemDataPreprocessor with default settings for SMILES column and filters.

        Parameters:
        smiles_col (str): The name of the column containing the SMILES strings. Default: 'Drug'
        filters (list of str): List of medchem rules or alerts to be applied. Default: ['rule_of_five', 'PAINS']
        """
        self.smiles_col = smiles_col
        self.filters = filters
    
    def get_available_filters(self):
        """
        Retrieves all available rules and alerts from the medchem library.

        Returns:
        dict: Dictionary containing two keys 'rules' and 'alerts', each holding a list of available filters.
        """
        available_rules = mc.rules.RuleFilters.list_available_rules().name.tolist()
        available_alerts = mc.structural.CommonAlertsFilters.list_default_available_alerts().rule_set_name.tolist()
        logging.info(f"Available rules: {available_rules}")
        logging.info(f"Available alerts: {available_alerts}")
        return {'rules': available_rules, 'alerts': available_alerts}

    def apply_medchem_filters(self, data, inplace=False):
        """
        Apply medicinal chemistry filters to compounds (SMILES) in the DataFrame.

        This method modifies the DataFrame by adding new columns that indicate whether each compound passes
        or fails the specified medicinal chemistry filters. The operation can be performed either in-place
        or on a copy of the data, depending on the value of the `inplace` parameter.

        Parameters:
        data (pd.DataFrame): The DataFrame containing the list of SMILES strings. It must include
                             a column specified by `self.smiles_col` which contains the SMILES data.
        inplace (bool): If True, modifies the DataFrame in-place and returns None. If False, returns a new
                        DataFrame with the modifications and leaves the original DataFrame unchanged.

        Returns:
        pd.DataFrame or None: The modified DataFrame if `inplace=False`, or None if `inplace=True`.

        Raises:
        Exception: Describes specific exceptions related to filter applications, such as failures in molecular
                   conversion, rule application errors, etc., with detailed error messages logged.

        Examples:
        >>> df = pd.DataFrame({'Drug': ['CCO', 'NCCO', 'CCN']})
        >>> processor = ChemDataPreprocessor()
        >>> new_df = processor.apply_medchem_filters(df, inplace=False)
        >>> # Now new_df contains the results of the filtering, and df is unchanged

        >>> # To modify df directly:
        >>> processor.apply_medchem_filters(df, inplace=True)
        >>> # Now df has been modified to include the results of the filtering
        """
        
        if not inplace:
            data = data.copy()
            
        # List available rules and alerts from medchem library
        available_rules, available_alerts = self.get_available_filters()['rules'], self.get_available_filters()['alerts']
        
        # Split filters list into rules and alerts, which will be applied via different functions in medchem module
        rules = [f for f in self.filters if f in available_rules]
        alerts = [f for f in self.filters if f in available_alerts]
        
        logging.info(f"Available rules: {available_rules}")
        logging.info(f"Available alerts: {available_alerts}")
        logging.info(f"Selected rules to apply: {rules}")
        logging.info(f"Selected alerts to apply: {alerts}")

        if rules or alerts:
            logging.info("Converting smiles to mol objects for applying medchem filters...")
            data["mol"] = data[self.smiles_col].apply(dm.to_mol)

        # Apply rules
        if rules:
            logging.info(f"Applying the following medicinal chemistry rules: {rules}")
            rfilter = mc.rules.RuleFilters(rule_list=rules)
            try:
                results = rfilter(
                    mols=data["mol"].tolist(),
                    n_jobs=-1,
                    progress=True,
                    progress_leave=True,
                    scheduler="auto",
                    keep_props=False,
                    fail_if_invalid=True,
                )
                for r in rules:
                    data[r] = results[r].tolist()
            except Exception as e:
                logging.error(f"Error applying medchem rules: {str(e)}")

        # Apply alerts
        if alerts:
            logging.info(f"Applying the following structural alerts: {alerts}")
            for a in alerts:
                try:
                    results = mc.functional.alert_filter(
                        mols=data["mol"].tolist(),
                        alerts=[a],
                        n_jobs=-1,
                        progress=True,
                    )
                    data[a] = list(results)
                except Exception as e:
                    logging.error(f"Error applying alert {a}: {str(e)}")
        if not inplace:
            return data

