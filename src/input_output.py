import json

import pandas as pd
from models import Config, InputConfig, Inputs


CONFIG_PATH = './input_config.json'

def load_config() -> InputConfig:
  with open(CONFIG_PATH) as f:
    return InputConfig([Config(**conf) for conf in json.load(f)])

def get_inputs(config: InputConfig) -> Inputs:
  out = {}
  for conf in config.config:
    in_ = input(conf.prompt + '\n') 
    out[conf.name] = in_ if in_ else conf.default
  return Inputs(**out)

def load_data(inputs: Inputs) -> pd.DataFrame:
  try:
    data = pd.read_csv(inputs.path_to_sheet)
  except FileNotFoundError:
    raise Exception('File not found at the location specified!')
  except pd.errors.ParserError:
    raise Exception("""
                    The selected file is invalid.
                    Make sure you provide a valid csv file.
                    """)
  return data