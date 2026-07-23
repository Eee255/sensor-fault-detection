import os
import sys
import pickle

import numpy as np

from sensor_fault_detection.exception import SensorException
from sensor_fault_detection.logger import logging


def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """Save numpy array data to file, creating parent dirs as needed."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
        logging.info(f"Saved numpy array to file: {file_path}")
    except Exception as e:
        raise SensorException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """Load numpy array data from file."""
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    """Pickle a Python object to file, creating parent dirs as needed."""
    try:
        logging.info("Entered the save_object method of main_utils")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of main_utils")
    except Exception as e:
        raise SensorException(e, sys) from e


def load_object(file_path: str) -> object:
    """Unpickle a Python object from file."""
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e