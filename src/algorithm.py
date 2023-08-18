
import numpy as np
import pandas as pd
from progress.bar import IncrementalBar

from models import Inputs, Options


def sample_from_pool(generator: np.random.Generator, pool: np.ndarray) -> tuple[int, np.ndarray]:
  choice = generator.choice(np.argwhere(pool))[0]
  pool[choice] = 0
  return choice, pool

def pick_best_candidate(
  connection_matrix: pd.DataFrame, solution: list[list[int]],
  table: int, pool: np.ndarray
) -> tuple[int, np.ndarray]:
  p_matrix = connection_matrix.iloc[solution[table]].sum().reset_index()[0]
  p_matrix[np.nonzero(pool == 0)[0]] = np.nan
  choice = p_matrix.idxmax()
  pool[choice] = 0
  return choice, pool

def greedy_generator(
  connection_matrix: pd.DataFrame, options: Options, generator: np.random.Generator,
) -> list[list[int]]:

  tables = range(options.max_tables)
  pool = np.ones(options.tot_guests)
  solution: list[list[int]] = [[] for _ in tables]

  for table in tables:
    while len(solution[table]) < int(options.max_guests_per_table):
      if pool.sum() == 0:
        return solution
      if len(solution[table]) == 0: 
        choice, pool = sample_from_pool(generator, pool)
        solution[table].append(choice)
      else:
        choice, pool = pick_best_candidate(connection_matrix, solution, table, pool)
        solution[table].append(choice)
  return solution

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
    max_tables=np.ceil(tot_guests / int(inputs.min_guests_per_table)).astype(int),
    max_guests_per_table=int(inputs.max_guests_per_table),
    min_guests_per_table=int(inputs.min_guests_per_table),
    tot_guests=tot_guests,
    num_iterations=int(inputs.num_iterations)
  )

def run_greedy_algorithm(
  options: Options, connection_matrix: pd.DataFrame
) -> dict[str, list]:

  results: dict[str, list] = {
    'solution': [],
    'score': [],
  }

  num_iterations = (
    options.num_iterations if options.num_iterations > 0
    else options.tot_guests * options.max_tables
  )

  with IncrementalBar('Optimizing seating', max=num_iterations) as bar:
    for ii in range(num_iterations):
      generator = np.random.default_rng(seed=ii*10000)
      sol = greedy_generator(connection_matrix, options, generator)
      results['solution'].append(sol)
      results['score'].append(fitness_fun(sol, connection_matrix))
      bar.next()
    bar.finish()
  return results

def display_results(results: dict[str, list], options: Options, data: pd.DataFrame) -> None:
  results_df = pd.DataFrame(results) 
  id_max = results_df['score'].idxmax()
  print('Max score: ', results_df['score'][id_max])
  [
    print(
      f'Table {ii}:\n',
      data.loc[[*results_df['solution'][id_max][ii]], ['name', 'lastName']]
    ) for ii in range(options.max_tables)
  ]
