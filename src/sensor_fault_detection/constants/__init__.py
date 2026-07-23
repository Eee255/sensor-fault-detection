import os
import numpy as np

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



# ---- Data Validation related constants ----
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"


TARGET_COLUMN: str = "class"
TARGET_COLUMN_MAPPING: dict = {"pos": 1, "neg": 0}

# -------- Data Transformation -------
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_OBJECT_FILE_NAME: str = "preprocessing.pkl"

# Transformed splits are NumPy binaries written with np.save, so they carry
# the .npy extension — the model_trainer stage globs for *.npy, not *.py.
DATA_TRANSFORMATION_TRAIN_FILE_NAME: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_NAME: str = "test.npy"

# KNNImputer config. Sensor readings are correlated (pressure, temperature,
# cycle counts move together), so the 3 nearest neighbors estimate a missing
# value far better than a column median. n_neighbors=3 keeps it affordable
# at ~60k rows; weights="uniform" treats those 3 neighbors equally.
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}