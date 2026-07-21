from sensor_fault_detection.entity.config_entity import TrainingPipelineConfig, DataValidationConfig
from sensor_fault_detection.components.data_validation import DataValidation
from sensor_fault_detection.entity.artifact_entity import DataIngestionArtifact

pipeline_config = TrainingPipelineConfig()
validation_config = DataValidationConfig(pipeline_config)

# normally this comes from actually running DataIngestion,
# but for testing, you can point it at files you already have
ingestion_artifact = DataIngestionArtifact(
    trained_file_path="artifacts/07_21_2026_22_29_39/data_ingestion/ingested/train.csv",
    test_file_path="artifacts/07_21_2026_22_29_39/data_ingestion/ingested/test.csv"
)

validation = DataValidation(ingestion_artifact, validation_config)
artifact = validation.initiate_data_validation()

print(artifact)