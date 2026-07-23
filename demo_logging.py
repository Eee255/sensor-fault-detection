from sensor_fault_detection.logger import logging

logging.info("Starting demo pipeline run")
logging.info("data ingestion complete: 36000 records loaded")
logging.warning("validation found 2 missing columns")
logging.error("Pipeline failed during transformation step")
