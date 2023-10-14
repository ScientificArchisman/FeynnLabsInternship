from src_proj3.logger import logging
from src_proj3.exception import CustomException
from src_proj3.utils import save_pickle
import numpy as np
import sys
import pandas as pd
import os
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.impute import SimpleImputer


# Custom class to remove columns
class ColumnRemover:
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        res : pd.DataFrame =  X[self.columns]
        res.columns = res.columns
        return res

class DataTransformation:

    def __init__(self):
        self.numerical_columns : list = ['hour', 'dayofweek', 'quarter', 'month', 'year', 'dayofyear',
                                        'weekofmonth', 'weekofyear']
        
        self.reqd_columns : list = ['month', 'hour', 'dayofweek', 'dayofyear']
        
        self.root_data_file : str = os.path.join("artifacts", "transformed_data")
        self.root_preprocessor_file : str = os.path.join("artifacts", "preprocessor")
        self.train_features_path : str =  os.path.join(self.root_data_file, "train_features.csv")
        self.train_labels_path : str = os.path.join(self.root_data_file, "train_labels.csv")
        self.test_features_path : str = os.path.join(self.root_data_file, "test_features.csv")
        self.test_labels_path : str = os.path.join(self.root_data_file, "test_labels.csv")
    
    def get_data_preprocessor(self, k:int = 15):
        """Returns the preprocessor object and saves it in pkl format
        Args:
            k (int, optional): Number of features to select according to Mutual information. Defaults to 15.
        Returns:
            preprocessor: sklearn ColumnTransformer object
        """


        # Numerical pipeline
        numerical_pipeline = Pipeline(
            steps = [("imputer", SimpleImputer(strategy = "mean")),
                    ("scaler", StandardScaler())])

                
        # Column transformer
        transformer = ColumnTransformer([("num_pipeline", numerical_pipeline, self.reqd_columns)])
        
        # Mutual information feature selection
        overall_pipeline = Pipeline(steps = [("remover", ColumnRemover(self.reqd_columns)),
                                            ("transformer", transformer)])

        # Save the preprocessor
        os.makedirs(self.root_preprocessor_file, exist_ok=True)
        PREPROCESSOR_PATH = os.path.join(self.root_preprocessor_file, "preprocessor.pkl")
        save_pickle(overall_pipeline, PREPROCESSOR_PATH) 
        return overall_pipeline

    def initiate_data_transformation(self, train_data_file : str, test_data_file : str):
        """Transforms the data and saves it in artifacts
        Args:
            train_data_file (str): Path to train data
            test_data_file (str): Path to test data
        Returns:
            X_train (np.ndarray): Transformed training features
            X_test (np.ndarray): Transformed testing features
            y_train (np.ndarray): Transformed training labels
            y_test (np.ndarray): Transformed testing labels
        """
        try:
            logging.info("Loading data for transformation")
            train_data = pd.read_csv(train_data_file)
            test_data = pd.read_csv(test_data_file)
            logging.info("Data loaded successfully for transformation")
        except Exception as e:
            logging.error(f"Error loading data for transformation - {e}")

        # Split data into features and labels
        try:
            logging.info("Splitting data into features and labels")
            y_train = train_data["PJME_MW"]
            X_train = train_data.drop(columns=["PJME_MW"])
            logging.info("Training Data split successfully into features and labels")

            y_test = test_data["PJME_MW"]
            X_test = test_data.drop(columns=["PJME_MW"])
            logging.info("Testing Data split successfully into features and labels")

        except Exception as e:
            logging.error(f"Error splitting data into features and labels - {e}")
            sys.exit(1)

        # Get the preprocessor
        try:
            logging.info("Getting the preprocessor")
            preprocessor = self.get_data_preprocessor()
            logging.info("Preprocessor loaded successfully")
        
        except Exception as e:
            logging.error(f"Error loading preprocessor - {e}")
            sys.exit(1)

        # Fit the training set with the preprocessor
        try:
            logging.info("Fitting the training features set with the preprocessor")
            preprocessor.fit(X_train)
            logging.info("Training features set fitted successfully")
        except Exception as e:
            logging.error(f"Error fitting the training features set with the preprocessor - {e}")
            sys.exit(1)
        
            
        # Transform the training and testing dataset with the fitted preprocessor
        try:
            logging.info("Transforming the training and testing dataset with the fitted preprocessor")
            X_train = preprocessor.transform(X_train)
            y_train = y_train
            logging.info("Training set transformed successfully")
            X_test = preprocessor.transform(X_test)
            y_test = y_test
            logging.info("Testing set transformed successfully")
        except Exception as e:
            logging.error(f"Error transforming the training and testing dataset with the fitted preprocessor - {e}")
            sys.exit(1)

        # Save the transformed data
        try:
            logging.info("Saving the transformed data")
            os.makedirs(self.root_data_file, exist_ok=True)
            logging.info("Directory for transformed data created successfully")
            pd.DataFrame(X_train).to_csv(self.train_features_path, index = False)
            logging.info("Training features saved successfully")
            pd.DataFrame(y_train).to_csv(self.train_labels_path, index = False)
            logging.info("Training labels saved successfully")
            pd.DataFrame(X_test).to_csv(self.test_features_path, index = False)
            logging.info("Testing features saved successfully")
            pd.DataFrame(y_test).to_csv(self.test_labels_path, index = False)
            logging.info("Testing labels saved successfully")

        except Exception as e:
            logging.error(f"Error saving the transformed data - {e}")
            raise CustomException("Error saving the transformed data", sys)

        return (X_train, X_test, y_train, y_test)




    def __str__(self):
        return f"DataTransformation class object created at {self.PREPROCESSOR_PATH}"
    


if __name__ == "__main__":
    data_transform = DataTransformation()
    data_transform.get_data_preprocessor()
    data_transform.initiate_data_transformation("/Users/archismanchakraborti/Desktop/python_files/FeynnLabsInternship/Project3/artifacts/data/train_data.csv",
                                                "/Users/archismanchakraborti/Desktop/python_files/FeynnLabsInternship/Project3/artifacts/data/test_data.csv")
 