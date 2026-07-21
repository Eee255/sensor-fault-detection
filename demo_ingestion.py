import sys
from sensor_fault_detection.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor_fault_detection.components.data_ingestion import DataIngestion
from sensor_fault_detection.exception import SensorException


try:
    pipeline_config = TrainingPipelineConfig()
    ingestion_config = DataIngestionConfig(pipeline_config)
    ingestion = DataIngestion(ingestion_config)
    artifact = ingestion.initiate_data_ingestion()
    print(artifact)
except Exception as e:
    raise SensorException(e, sys)



'''
DataIngestionArtifact(trained_file_path='artifacts\\07_21_2026_22_29_39\\data_ingestion\\ingested\\train.csv', test_file_path='artifacts\\07_21_2026_22_29_39\\data_ingestion\\ingested\\test.csv')
'''