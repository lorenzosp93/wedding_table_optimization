from dataclasses import dataclass
from typing import LiteralString

parameters = [
  'partner',
  'preferences',
  'dislikes',
  'languages',
  'age',
  'city',
  'interests',
  'lastName'
]

inputs_names = [
  'path_to_sheet',
  'max_guests_per_table',
  'min_guests_per_table',
  'weight_partner',
  'weight_preferences',
  'weight_dislikes',
  'weight_languages',
  'weight_age',
  'weight_city',
  'weight_interests',
  'weight_lastName'
]


@dataclass
class Config:
  name: LiteralString
  verbose_name: str
  prompt: str
  default: str

@dataclass
class InputConfig:
  config: list[Config]

@dataclass
class Inputs:
  path_to_sheet: str
  max_guests_per_table: str
  min_guests_per_table: str
  weight_partner: str
  weight_preferences: str
  weight_dislikes: str
  weight_languages: str
  weight_age: str
  weight_city: str
  weight_interests: str
  weight_lastName: str
  num_iterations: str

@dataclass
class ParameterWeights:
  partner: int
  preferences: int
  dislikes: int
  languages: int
  age: int
  city: int
  interests: int
  lastName: int

@dataclass
class Options:
  max_tables: int
  max_guests_per_table: int
  min_guests_per_table: int
  tot_guests: int
  num_iterations: int
