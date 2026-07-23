from sensor_fault_detection.components.data_validation import DataValidation
from sensor_fault_detection.components.data_transformation import DataTransformation
from sensor_fault_detection.entity.config_entity import (
    TrainingPipelineConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from sensor_fault_detection.entity.artifact_entity import DataIngestionArtifact

if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()

    # Reuse whatever DataIngestionArtifact your demo_validation.py already
    # produces/loads — swap this in for the real one from that stage.
    data_ingestion_artifact = DataIngestionArtifact(
        trained_file_path="artifacts/07_21_2026_22_29_39/data_ingestion/ingested/train.csv",
        test_file_path="artifacts/07_21_2026_22_29_39/data_ingestion/ingested/test.csv"
    )

    data_validation_config = DataValidationConfig(training_pipeline_config)
    data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
    data_validation_artifact = data_validation.initiate_data_validation()

    data_transformation_config = DataTransformationConfig(training_pipeline_config)
    data_transformation = DataTransformation(
        data_validation_artifact, data_transformation_config
    )
    data_transformation_artifact = data_transformation.initiate_data_transformation()

    print(data_transformation_artifact)