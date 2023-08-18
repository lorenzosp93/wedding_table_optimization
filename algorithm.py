
import numpy as np
import pandas as pd

from models import Inputs, Options


def sample_from_pool(generator: np.random.Generator, pool: np.ndarray) -> int:
  choice = generator.choice(np.argwhere(pool))[0]
  pool[choice] = 0
  return choice

def pick_best_candidate(
  connection_matrix: pd.DataFrame, solution: list[list[int]],
  table: int, pool: np.ndarray
) -> int:
  p_matrix = connection_matrix.iloc[solution[table]].sum().reset_index()[0]
  p_matrix[np.nonzero(pool == 0)[0]] = 0
  choice = p_matrix.idxmax()
  pool[choice] = 0
  return choice

def greedy_generator(
  connection_matrix: pd.DataFrame, options: Options,
  random_seed:int=0,
) -> list[list[int]]:
  generator = np.random.default_rng(seed=random_seed)
  tables = range(options.max_tables)
  pool = np.ones(options.tot_guests)
  solution: list[list[int]] = [[] for _ in tables]

  for table in tables:
    while len(solution[table]) < int(options.max_guests_per_table):
      if pool.sum() == 0:
        return solution
      if len(solution[table]) == 0: 
        solution[table].append(sample_from_pool(generator, pool))
      else:
        solution[table].append(
          pick_best_candidate(connection_matrix, solution, table, pool)
        )
  return [[]]

def fitness_fun(solution: list[list[int]], connection_matrix: pd.DataFrame):
  return sum(
    sum(
      connection_matrix.iloc[j, k]
      for j in solution[table] for k in solution[table] if j>k
    ) for table in range(len(solution))
  )

def get_options(inputs: Inputs, data: pd.DataFrame) -> Options:
  tot_guests = data.index.size
  return Options(
    max_tables=np.ceil(tot_guests / int(inputs.min_guests_per_table)),
    max_guests_per_table=int(inputs.max_guests_per_table),
    min_guests_per_table=int(inputs.min_guests_per_table),
    tot_guests=tot_guests,
    num_iterations=int(inputs.num_iterations)
  )

def get_nonzero_connection_matrix(connection_matrix: pd.DataFrame) -> pd.DataFrame:
  return connection_matrix - connection_matrix.min() + 1

def run_greedy_algorithm(
  options: Options, connection_matrix: pd.DataFrame
) -> dict[str, list]:
  connection_matrix = get_nonzero_connection_matrix(connection_matrix)
  results: dict[str, list] = {
    'solution': [],
    'score': [],
  }
  for ii in range(options.num_iterations):
    sol = greedy_generator(connection_matrix, options, ii)
    results['solution'].append(sol)
    results['score'].append(fitness_fun(sol, connection_matrix))
  return results

def display_results(results: dict[str, list], options: Options, data: pd.DataFrame) -> None:
  results_df = pd.DataFrame(results) 
  id_max = results_df['score'].idxmax()
  print('Max score: ', results_df['score'][id_max])
  [
    print(
      f'Table {ii}:\n',
      data.index[results_df['solution'][id_max][ii]]
    ) for ii in range(options.max_tables)
  ]
