import os
import sys
import pandas as pd
from scipy.stats import ks_2samp

from sensor_fault_detection.entity.config_entity import DataValidationConfig
from sensor_fault_detection.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor_fault_detection.exception import SensorException
from sensor_fault_detection.logger import logging
from sensor_fault_detection.constants import SCHEMA_FILE_PATH

import yaml


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = self.read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        try:
            with open(file_path, "rb") as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """Schema check: does the dataframe have the expected number of columns?"""
        try:
            expected_columns = len(self._schema_config["Columns"])
            actual_columns = len(dataframe.columns)
            return actual_columns == expected_columns
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame) -> bool:
        try:
            report = {}
            drift_found = False
            threshold = 0.05 / len(base_df.columns) 

            for column in base_df.columns:
                d1 = base_df[column].dropna()
                d2 = current_df[column].dropna()

                if len(d1) == 0 or len(d2) == 0:
                    # not enough real data to compare — be HONEST about it
                    report[column] = {
                        "p_value": None,
                        "drift_detected": None,   
                        "note": "insufficient non-null data to run KS test"
                    }
                    continue

                result = ks_2samp(d1, d2)
                is_drift = bool(result.pvalue < threshold)

                if is_drift:
                    drift_found = True

                report[column] = {
                    "p_value": float(result.pvalue),
                    "drift_detected": is_drift
                }

            dir_path = os.path.dirname(self.data_validation_config.drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            with open(self.data_validation_config.drift_report_file_path, "w") as f:
                yaml.dump(report, f)

            return drift_found
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # ---- SCHEMA CHECK: hard gate ----
            status = self.validate_number_of_columns(train_df)
            status_test = self.validate_number_of_columns(test_df)
            validation_status = status and status_test

            if not validation_status:
                # save the rejected files first, so there's a paper trail
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                train_df.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
                test_df.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)

                raise Exception(
                    f"Data validation failed — schema mismatch. "
                    f"Rejected data saved at {self.data_validation_config.invalid_data_dir}"
                )

            # ---- only reaches here if schema check PASSED ----
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # ---- DRIFT CHECK: soft warning, does NOT stop the pipeline ----
            drift_status = self.detect_dataset_drift(train_df, test_df)

            if drift_status:
                logging.warning(
                    f"Data drift detected. See report at {self.data_validation_config.drift_report_file_path}"
                )
            else:
                logging.info("No data drift detected.")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                drift_status=drift_status,
            )
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)