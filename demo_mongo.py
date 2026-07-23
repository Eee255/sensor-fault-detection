import certifi
from pymongo import MongoClient
import sys
import os

from sensor_fault_detection.logger import logging
from sensor_fault_detection.exception import SensorException


try:
    mongo_url = os.getenv("MONGODB_URL")
    client = MongoClient(mongo_url, tlsCAFile=certifi.where())
    client.admin.command("ping")
    logging.info("MongoDB connection successful")
    print("Connected to MongoDB Atlas")
except Exception as e:
    raise SensorException(e, sys)