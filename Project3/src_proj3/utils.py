import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.logger import logging

def save_pickle(preprocessor, filename):
    """
    Save a scikit-learn object to a file using pickle.
    
    Parameters:
        preprocessor (scikit-learn transformer): The preprocessor object to be saved.
        filename (str): The name of the file to save the preprocessor object to.
    """
    try:
        with open(filename, 'wb') as f:
            pickle.dump(preprocessor, f)
        logging.info(f"Preprocessor saved to {filename}")
    except Exception as e:
        logging.error("Error saving preprocessor: %s", e)

def load_pickle(filename):
    """
    Load a scikit-learn preprocessor object from a file using pickle.
    
    Parameters:
        filename (str): The name of the file to load the preprocessor object from.
        
    Returns:
        preprocessor (scikit-learn transformer): The loaded preprocessor object.
    """
    try:
        with open(filename, 'rb') as f:
            preprocessor = pickle.load(f)
        logging.info(f"Preprocessor loaded from {filename}")
        return preprocessor
    except Exception as e:
        logging.error("Error loading preprocessor: %s", e)
        return None


