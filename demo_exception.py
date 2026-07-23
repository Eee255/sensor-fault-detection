import sys

from sensor_fault_detection.logger import logging
from sensor_fault_detection.exception import SensorException

try:
    result = 1 / 0
except Exception as e:
    logging.error("Division step failed, wrapping and re-raising")
    raise SensorException(e, sys)