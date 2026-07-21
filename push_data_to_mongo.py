import os
import sys

import certifi
import pandas as pd
from pymongo import MongoClient

from sensor_fault_detection.logger import logging
from sensor_fault_detection.exception import SensorException

DATABASE_NAME = "sensor_db"
COLLECTION_NAME = "sensor_readings"
FILE_PATH = "data/aps_failure_training_set.csv"

try:
    mongo_url = os.getenv("MONGODB_URL")
    if mongo_url is None:
        raise ValueError("MONGODB_URL environment variable is not set")

    df = pd.read_csv(FILE_PATH, skiprows=20)  
    logging.info(f"CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    records = df.to_dict(orient="records")

    client = MongoClient(mongo_url, tlsCAFile=certifi.where())
    collection = client[DATABASE_NAME][COLLECTION_NAME]

    BATCH_SIZE = 5000
    total_inserted = 0
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start:start + BATCH_SIZE]
        result = collection.insert_many(batch)
        total_inserted += len(result.inserted_ids)
        logging.info(f"Batch {start // BATCH_SIZE + 1}: {total_inserted} total documents inserted")

    print(f"Inserted {total_inserted} documents")

except Exception as e:
    raise SensorException(e, sys)