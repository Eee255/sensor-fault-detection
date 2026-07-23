import sys

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from sensor_fault_detection.constants import (
    TARGET_COLUMN,
    TARGET_COLUMN_MAPPING,
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)
from sensor_fault_detection.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from sensor_fault_detection.entity.config_entity import DataTransformationConfig
from sensor_fault_detection.exception import SensorException
from sensor_fault_detection.logger import logging
from sensor_fault_detection.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def _encode_target(target: pd.Series) -> pd.Series:
        """
        Map string labels to ints via TARGET_COLUMN_MAPPING using .map (not
        .replace — pandas 3.0 downcasts silently on .replace). .map turns any
        label outside the mapping into NaN, so we fail loudly instead of
        letting a stray label poison the target column.
        """
        try:
            encoded = target.map(TARGET_COLUMN_MAPPING)
            if encoded.isna().any():
                unknown = sorted(target[encoded.isna()].unique().tolist())
                raise ValueError(
                    f"Unmapped target label(s) {unknown}; "
                    f"expected one of {list(TARGET_COLUMN_MAPPING)}"
                )
            return encoded.astype(int)
        except Exception as e:
            raise SensorException(e, sys) from e

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Single-step Pipeline wrapping KNNImputer. Kept as a Pipeline (not a
        bare transformer) so a scaler or other step can be inserted later
        without changing the saved-object contract or any call site.
        """
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            return Pipeline(steps=[("imputer", imputer)])
        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = self._encode_target(train_df[TARGET_COLUMN])

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = self._encode_target(test_df[TARGET_COLUMN])

            preprocessor = self.get_data_transformer_object()

            # Fit ONLY on train. Test — and later, a single row hitting the
            # inference endpoint — always gets .transform(), never
            # fit_transform(). This one line is what prevents
            # training/serving skew.
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_df
            )
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            train_arr = np.c_[
                transformed_input_train_feature, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_df)
            ]

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )
            # The fitted preprocessor — this is what travels with the model
            # to production. Serving code loads it and calls .transform()
            # on incoming rows; it must never be re-fit there.
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e