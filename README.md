# Wedding table optimization

Simple optimization model running a Greedy Heuristic to determine the most optimal table arrangement, given a set of parameters, and some information on the guests.

Multiple optimization strategies were evaluated, such as

* Mixed Integer Linear Programming
* Genetic Algorithm
* Greedy Heuristic
* Greedy Heuristic Seeded Genetic Algorithm

see the `Tables Optimization.ipynb` notebook for more information.

Ultimately the Greedy Heuristic proved to vastly outperform the other approaches both in term of results, and in terms of speed.

## Guest relationship modeling

The guests are modeled by supplying a `.csv` file with the following columns:

| Parameter   | Format  | Example                   | Default weight | Comment                                                                                                  |
|-------------|---------|---------------------------|----------------|----------------------------------------------------------------------------------------------------------|
| name        | string  | Lorenzo                   | n/a            | Only used for rendering outputs                                                                          |
| lastName    | string  | Spinelli                  | 20             | People with the same last name will be likelier to be seated together.                                   |
| partner     | integer | 1                         | 6000           | **Zero-based index** of the guest's partner in the list (if applicable).                                 |
| preferences | integer | 5                         |  800           | **Zero-based index**  of the guest's preferred table companion in the list (if applicable).              |
| dislikes    | integer | 9                         | -1200          | **Zero-based index**  of the guest's undesired table companion in the list (if applicable).              |
| languages   | string[^1] | italian\|english,spanish  | 500            | List of languages spoken fluently by the guest.                                                          |
| age         | integer | 30                        | -300           | Age of the guest. Based on the weight, large gaps will be avoided (if negative).                         |
| city        | string[^1] | Amsterdam,NL              | 50             | City of residence of the guest. People from the same city or country are likelier to be seated together. |
| interests   | string[^1] | engineering;tech&politics | 100            | Key interests and hobbies. Guests with the same interests will be likelier to be seated together.        |


[^1]: the following separators are accepted: `,`, `;`, `&`, `|`, `-`, `+`.

You can find an example `testing.csv` file in the root of this repository.

## Usage

A shell script is provided for UNIX users. You can simply run the following command:

```source tableOptim.sh```

The user will be prompted for the input parameters, and the most optimal seating disposition will be displayed.

### Input parameters

The following inputs are supported:

* path to the guest modeling spreadsheet
* maximum number of guests per table
* parameter weights
* number of random iterations of the algorithm (`default = tot_guests * 2`).
