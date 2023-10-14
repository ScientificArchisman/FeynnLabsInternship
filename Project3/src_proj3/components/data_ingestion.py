import os
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from src_proj3.exception import CustomException
from src_proj3.logger import logging


    
class DataIngestion:

    def __init__(self, data_path) -> None:
        self.data_path : str = data_path
        self.root_data_file : str = os.path.join("artifacts", "data")
        self.test_data_file : str = os.path.join(self.root_data_file, "test_data.csv")
        self.train_data_file : str = os.path.join(self.root_data_file, "train_data.csv")
        self.raw_data_file : str = os.path.join(self.root_data_file, "raw_data.csv")

    def create_features(self, df):
         """ 
         Create time series features based on time series index.
         """
         df['hour'] = df.index.hour
         df['dayofweek'] = df.index.dayofweek
         df['quarter'] = df.index.quarter
         df['month'] = df.index.month
         df['year'] = df.index.year
         df['dayofyear'] = df.index.dayofyear
         df['weekofmonth'] = df.index.day
         df['weekofyear'] = df.index.isocalendar().week
         return df

    
    logging.info("Entering data ingestion")
    def initiate_data_split(self):
        os.makedirs(self.root_data_file, exist_ok=True)
        
        try:
            raw_data = pd.read_csv(self.data_path)
            raw_data = raw_data.set_index('Datetime')
            raw_data.index = pd.to_datetime(raw_data.index)

        except Exception as e:  
            logging.error("Error reading data")
            raise CustomException(e, sys)
        
        logging.info("Splitting data into train and test")
        raw_data = self.create_features(raw_data)
        train_data, test_data = train_test_split(raw_data, test_size=0.2, random_state=42)

        try:
            logging.info("Saving data to artifacts")
            train_data.to_csv(self.train_data_file, index=False)
            test_data.to_csv(self.test_data_file, index=False)
            raw_data.to_csv(self.raw_data_file, index=False)
        except Exception as e:
            logging.error("Error saving data to artifacts")
            raise CustomException(e, sys)


        return self.train_data_file, self.test_data_file, self.raw_data_file
    

if __name__ == "__main__":
    data_ingestion = DataIngestion("/Users/archismanchakraborti/Desktop/python_files/FeynnLabsInternship/Project3/archive/PJME_hourly.csv")
    data_ingestion.initiate_data_split()
