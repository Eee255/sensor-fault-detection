import os
import sys
import certifi
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split


from sensor_fault_detection.logger import logging
from sensor_fault_detection.exception import SensorException
from sensor_fault_detection.entity.config_entity import DataIngestionConfig
from sensor_fault_detection.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL = os.getenv("MONGODB_URL")



class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """Read every document from MongoDB and return it as a DataFrame."""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            client = MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            collection = client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            # Mongo adds an "_id" column automatically — we don't need it
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            # some datasets use "na" as a string instead of real NaN — clean that up
            df.replace({"na": np.nan}, inplace=True)

            return df
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Save the raw snapshot to feature_store_file_path. Return the dataframe."""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # make sure the folder exists before saving into it
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """Split into train/test and write both CSVs."""
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            training_file_path = self.data_ingestion_config.training_file_path
            testing_file_path = self.data_ingestion_config.testing_file_path

            # make sure the folder exists before saving into it
            dir_path = os.path.dirname(training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(training_file_path, index=False, header=True)
            test_set.to_csv(testing_file_path, index=False, header=True)

            logging.info("Exported train and test file paths")
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """Run the three steps above, return the artifact."""
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)