import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.pipeline import Pipeline
from build.lib.src.utils import export_collection_as_dataframe
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            # Define custom function to replace 'na' with np.nan
            replace_na_with_nan = lambda X: np.where(X == 'na', np.nan, X)

            # Define preprocessing steps
            nan_replacement_step = ('nan_replacement', FunctionTransformer(replace_na_with_nan))
            imputer_step = ('imputer', SimpleImputer(strategy='constant', fill_value=0))
            scaler_step = ('scaler', RobustScaler())

            preprocessor = Pipeline(
                steps=[
                    nan_replacement_step,
                    imputer_step,
                    scaler_step
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info(f"Train DataFrame Columns: {train_df.columns.tolist()}")
            logging.info(f"Test DataFrame Columns: {test_df.columns.tolist()}")

            target_column_name = "Good/Bad"
            if target_column_name not in train_df.columns or target_column_name not in test_df.columns:
                raise CustomException(f"Target column '{target_column_name}' not found in dataset columns. Available columns: {train_df.columns.tolist()}", sys)

            preprocessor = self.get_data_transformer_object()

            # Map '+1' to 0 and '-1' to 1
            target_column_mapping = {"+1": 0, "-1": 1}


            # Separate input features and target
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name].map(target_column_mapping)

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name].map(target_column_mapping)

            # Check for NaN in target after mapping
            if target_feature_train_df.isnull().any() or target_feature_test_df.isnull().any():
                unexpected_train = train_df[target_column_name][target_feature_train_df.isnull()].unique()
                unexpected_test = test_df[target_column_name][target_feature_test_df.isnull()].unique()

                raise CustomException(
                    f"Unmapped target labels found. Train labels: {unexpected_train}, Test labels: {unexpected_test}",
                    sys
                )

            # Apply preprocessing
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            # Handle imbalanced data
            smt = SMOTETomek(sampling_strategy="minority", smote=SMOTE(k_neighbors=1))

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                transformed_input_train_feature, target_feature_train_df
            )

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                transformed_input_test_feature, target_feature_test_df
            )

            # Combine features and targets
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            # Save the preprocessor object
            save_object(self.data_transformation_config.preprocessor_obj_file_path, obj=preprocessor)

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
