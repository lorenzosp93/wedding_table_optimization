import numpy as np
import pandas as pd

from models import Inputs, ParameterWeights

REGEX_REPLACE_SEPARATORS = ",|\||&|-|\+|;"


def setup_parameter_weights(inputs: Inputs) -> ParameterWeights:
    keys = [key for key in dir(inputs) if key.startswith("weight")]
    val = {key.split("_")[-1]: getattr(inputs, key) for key in keys}
    return ParameterWeights(**val)


def normalize_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    return np.nan_to_num((matrix - matrix.mean()) / matrix.std())


def calc_encoded_col(column: pd.Series) -> pd.DataFrame:
    replaced_string_array = column.str.replace(
        REGEX_REPLACE_SEPARATORS, "|"
    ).str.replace(" ", "")
    encoded_array = replaced_string_array.str.get_dummies()
    encoded_matrix = encoded_array @ encoded_array.T
    return normalize_matrix(encoded_matrix)


def calc_age(data: pd.DataFrame) -> pd.DataFrame:
    age_matrix = np.abs(data.age.array - data.age.array[:, None])
    return normalize_matrix(
        pd.DataFrame(age_matrix, index=data.index, columns=data.index)
    )


def calc_target_col(column: pd.Series, index: pd.Index) -> pd.DataFrame:
    target_matrix = column.to_numpy() == np.arange(column.size)[:, None]
    return pd.DataFrame(target_matrix, index=index, columns=index)


def calc_connection_matrix(data: pd.DataFrame, weights: ParameterWeights) -> np.ndarray:
    coefficient_matrix = {}
    coefficient_matrix["languages"] = calc_encoded_col(data.languages)
    coefficient_matrix["city"] = calc_encoded_col(data.city)
    coefficient_matrix["interests"] = calc_encoded_col(data.interests)
    coefficient_matrix["lastName"] = calc_encoded_col(data.lastName)
    coefficient_matrix["age"] = calc_age(data)
    coefficient_matrix["partner"] = calc_target_col(data.partner, data.index)
    coefficient_matrix["preferences"] = calc_target_col(data.preferences, data.index)
    coefficient_matrix["dislikes"] = calc_target_col(data.dislikes, data.index)
    return normalize_matrix(
        sum(
            [
                coefficient_matrix[key] * int(val)
                for key, val in weights.__dict__.items()
            ]
        )
    ).to_numpy()
