import os

# Database
DATABASE_NAME: str = "sensor_db"
COLLECTION_NAME: str = "sensor_readings"

# Target column
TARGET_COLUMN: str = "class"

# Common file names
FILE_NAME: str = "sensor.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

# Pipeline / artifact directory structure
ARTIFACT_DIR: str = "artifacts"
PIPELINE_NAME: str = "sensor_pipeline"

# Data ingestion constants
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2