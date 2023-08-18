from algorithm import display_results, get_options, run_greedy_algorithm
from data_manipulation import calc_connection_matrix, setup_parameter_weights
from input_output import get_inputs, load_config, load_data

def main():
  # load configuration from json file
  config = load_config()
  # read input from I/O
  inputs = get_inputs(config)
  # load data from input CSV file
  data = load_data(inputs)
  # create weights based on input choices
  parameter_weights = setup_parameter_weights(inputs)
  # calculate the connection matrix based on data and weights
  connection_matrix = calc_connection_matrix(data, parameter_weights)
  # fill out the options from the inputs
  options = get_options(inputs, data)
  # compute the results
  results = run_greedy_algorithm(options, connection_matrix)
  # display the results
  display_results(results, options, data)


if __name__ == "__main__":
  main()
