

import numpy as np
import pandas as pd

from models import Inputs, ParameterWeights


def setup_parameter_weights(inputs: Inputs) -> ParameterWeights:
  keys = [key for key in dir(inputs) if key.startswith('weight')]
  val = {key.split('_')[-1]: getattr(inputs, key) for key in keys}
  return ParameterWeights(**val)

def normalize_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
  return (matrix - matrix.mean()) / matrix.std()

def calc_encoded_col(column: pd.Series) -> pd.DataFrame:
  encoded_array = column.str.get_dummies()
  encoded_matrix = encoded_array @ encoded_array.T
  return normalize_matrix(encoded_matrix)

def calc_lastName(data: pd.DataFrame) -> pd.DataFrame:
  lastName_array = data.reset_index().lastName.str.split(' ').str.join('|')
  lastName_matrix = calc_encoded_col(lastName_array)
  lastName_matrix.set_index(data.index, inplace=True)
  lastName_matrix.columns = data.index 
  return normalize_matrix(lastName_matrix)

def calc_age(data: pd.DataFrame) -> pd.DataFrame:
  age_matrix = np.abs(data.age.array - data.age.array[:, None])
  return normalize_matrix(pd.DataFrame(age_matrix, index=data.index, columns=data.index))

def calc_target_col(column: pd.Series, index: pd.Index) -> pd.DataFrame:
  target_matrix = column.array == np.arange(column.size)[:, None]
  return pd.DataFrame(target_matrix, index=index, columns=index)

def calc_connection_matrix(data: pd.DataFrame, weights: ParameterWeights) -> pd.DataFrame:
  coefficient_matrix = {}
  coefficient_matrix['languages'] = calc_encoded_col(data.languages)
  coefficient_matrix['city'] = calc_encoded_col(data.city)
  coefficient_matrix['interests'] = calc_encoded_col(data.interests)
  coefficient_matrix['lastName'] = calc_lastName(data)
  coefficient_matrix['age'] = calc_age(data)
  coefficient_matrix['partner'] = calc_target_col(data.partner, data.index)
  coefficient_matrix['preferences'] = calc_target_col(data.preferences, data.index)
  coefficient_matrix['dislikes'] = calc_target_col(data.dislikes, data.index)
  return sum([
    coefficient_matrix[key] * val
    for key, val in weights.__dict__.items()
  ])