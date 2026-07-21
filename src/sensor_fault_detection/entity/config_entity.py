
import os
from datetime import datetime
from sensor_fault_detection.constants import (
    ARTIFACT_DIR,
    PIPELINE_NAME,
    FILE_NAME,
    TRAIN_FILE_NAME,
    TEST_FILE_NAME,
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_FEATURE_STORE_DIR,
    DATA_INGESTION_INGESTED_DIR,
    DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
    DATABASE_NAME,
    COLLECTION_NAME,
    DATA_VALIDATION_DIR_NAME,
    DATA_VALIDATION_VALID_DIR,
    DATA_VALIDATION_INVALID_DIR,
    DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
    DATA_VALIDATION_DRIFT_REPORT_DIR

)





class TrainingPipelineConfig:
    def __init__(self, timestamp: datetime = datetime.now()):
        timestamp_str = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp_str)
        self.timestamp: str = timestamp_str


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = COLLECTION_NAME
        self.database_name: str = DATABASE_NAME


class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path = os.path.join(
            self.valid_data_dir, TRAIN_FILE_NAME
        )
        self.valid_test_file_path = os.path.join(
            self.valid_data_dir, TEST_FILE_NAME
        )
        self.invalid_train_file_path = os.path.join(
            self.invalid_data_dir, TRAIN_FILE_NAME
        )
        self.invalid_test_file_path = os.path.join(
            self.invalid_data_dir, TEST_FILE_NAME
        )
        self.drift_report_file_path = os.path.join(
            self.data_validation_dir,
            DATA_VALIDATION_DRIFT_REPORT_DIR,
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )