import numpy as np
import pandas as pd
from itertools import chain
from progress.bar import IncrementalBar

from models import Inputs, Options, Solution, Results


def sample_from_pool(generator: np.random.Generator, pool: np.ndarray) -> np.int32:
    choice = generator.choice(np.argwhere(pool))[0]
    return choice


def pick_best_candidate(
    connection_matrix: np.ndarray,
    solution: Solution,
    options: Options,
) -> tuple[np.int32, np.int32]:
    p_matrix = np.stack(
        [
            connection_matrix[table, :].mean(axis=0)
            if len(table) < options.max_guests_per_table
            else np.array([np.nan] * options.tot_guests)
            for table in solution
        ]
    )
    p_matrix[:, np.fromiter(chain(*solution), np.int32)] = np.nan
    table, choice = np.unravel_index(np.nanargmax(p_matrix), p_matrix.shape)
    return table, choice


def pick_worst_candidate(connection_matrix: np.ndarray, solution: Solution) -> np.int32:
    p_matrix = connection_matrix[np.fromiter(chain(*solution), np.int32), :].sum(axis=0)
    return p_matrix.argmin()


def apply_choice(
    choice: np.int32, pool: np.ndarray, solution: Solution, table: np.int32
) -> tuple[Solution, np.ndarray]:
    pool[choice] = 0
    solution[table].append(choice)
    return solution, pool


def initialize_tables(
    tables: np.ndarray,
    connection_matrix: np.ndarray,
    options: Options,
    generator: np.random.Generator,
) -> tuple[Solution, np.ndarray]:
    pool = np.ones(options.tot_guests)
    solution: Solution = [[] for _ in tables]

    for table in tables:
        if table == 0:
            choice = sample_from_pool(generator, pool)
        else:
            choice = pick_worst_candidate(connection_matrix, solution)
        solution, pool = apply_choice(choice, pool, solution, table)
    return solution, pool


def greedy_generator_v2(
    connection_matrix: np.ndarray,
    options: Options,
    generator: np.random.Generator,
) -> Solution:
    tables = np.arange(options.max_tables)
    solution, pool = initialize_tables(tables, connection_matrix, options, generator)

    while pool.sum() > 0:
        table, choice = pick_best_candidate(connection_matrix, solution, options)
        solution, pool = apply_choice(choice, pool, solution, table)

    return solution


def fitness_fun(solution: Solution, connection_matrix: np.ndarray) -> float:
    return sum(
        sum(
            connection_matrix[j, k]
            for j in solution[table]
            for k in solution[table]
            if j > k
        )
        for table in range(len(solution))
    )


def get_options(inputs: Inputs, data: pd.DataFrame) -> Options:
    tot_guests = data.index.size
    return Options(
        max_tables=np.ceil(tot_guests / int(inputs.max_guests_per_table)).astype(int),
        max_guests_per_table=int(inputs.max_guests_per_table),
        tot_guests=tot_guests,
        num_iterations=int(inputs.num_iterations),
    )


def run_greedy_algorithm(options: Options, connection_matrix: np.ndarray) -> Results:
    results: Results = Results(
        solution=[],
        score=[],
    )

    num_iterations = (
        options.num_iterations if options.num_iterations > 0 else options.tot_guests * 2
    )

    with IncrementalBar("Optimizing seating", max=num_iterations) as bar:
        for ii in range(num_iterations):
            generator = np.random.default_rng(seed=ii * 10000)
            sol = greedy_generator_v2(connection_matrix, options, generator)
            results.solution.append(sol)
            results.score.append(fitness_fun(sol, connection_matrix))
            bar.next()
        bar.finish()
    return results


def display_results(results: Results, options: Options, data: pd.DataFrame) -> None:
    results_df = pd.DataFrame(results.__dict__)
    id_max = results_df["score"].idxmax()
    print("Max score: ", results_df["score"][id_max])
    [
        print(
            f"Table {ii}:\n",
            data.loc[[*results_df["solution"][id_max][ii]], ["name", "lastName"]],
        )
        for ii in range(options.max_tables)
    ]
