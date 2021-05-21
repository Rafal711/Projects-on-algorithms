import numpy as np
from prettytable import PrettyTable
import itertools

# A function that represents a decision matrix in table form.
def print_table(y, tab, N):
    labels = ['y(i-1)']
    j = 1
    for i in range(N, 0, -1):
        labels.extend([f'x{i}', f'f{j}(y{i-1})'])
        j += 1

    table = PrettyTable()
    table.field_names = labels

    y_c = np.array([y])
    compl_table = np.concatenate((y_c.T, tab), axis=1)
    for row in compl_table:
        table.add_row(row)
    print("\n")
    print(table)
    print("\n")

# A function that returns all possible solutions in table form.
def print_result(comb, N, etitle=' '):
    labels = [f'x{i+1}' for i in range(N)]
    table = PrettyTable()
    table.title = 'Solution' + etitle
    table.field_names = labels
    for row in comb:
        table.add_row(row)
    print("\n")
    print(table)
    print("\n")

"""
A function that extracts all possible solutions from the decision matrix.
Example: The chosen strategies are hidden in the form of columns of the following matrix.
Matrix = [[0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 1]]
Strategies -> [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 1)]
"""
def extract(x, state, row_nr, col_nr, y, tab, N, weights ,lst=None):
    if lst is None:
        lst = [[] for _ in range(N)]

    if x < N:

        if isinstance(tab[row_nr, col_nr], int):
            choice = tab[row_nr, col_nr]
            new_state = state - choice * weights[x]
            new_row_nr = np.where(y == new_state)[0][0]
            lst[x].append(choice)
            extract(x + 1, new_state, new_row_nr, col_nr - 2, y, tab, N, weights, lst)

        else:
            for choice in tab[row_nr, col_nr]:
                new_state = state - choice * weights[x]
                new_row_nr = np.where(y == new_state)[0][0]
                lst[x].append(choice)
                extract(x + 1, new_state, new_row_nr, col_nr - 2, y, tab, N, weights, lst)
                for i in range(len(lst) - 1, 0, -1):
                    while len(lst[i - 1]) < len(lst[i]):
                        lst[i - 1].append(lst[i - 1][-1])
    return list(zip(*lst))


def knapsack_prob(profit, weight, limit):
    N = len(weight)
    n = len(profit) - 1
    curr_idx = 0

    # column y_(i-1) expressing the acceptable states.
    y = np.array([i for i in range(limit + 1)])

    # Matrix that will contain the final result.
    tab = np.zeros((len(y), 2 * N), dtype=object)

    # Completion of first column.
    for i, _ in enumerate(tab[:, curr_idx]):
        if y[i] >= weight[n]:
            tab[i, curr_idx] = 1
            tab[i, curr_idx + 1] = profit[n]
    n -= 1
    curr_idx += 2

    # Filling the remaining columns.
    for _ in range(N-1):
        for i, _ in enumerate(tab[:, curr_idx]):
            # A case where there is no space to add another weight.
            if y[i] < weight[n]:
                tab[i, curr_idx] = 0
                tab[i, curr_idx + 1] = tab[i, curr_idx - 1]
            else:
                # Calculation of profit for the choice x = 0.
                opt_x0 = tab[i, curr_idx - 1]

                # Calculation of profit for the choice x = 1.
                row_idx = np.where(y == (y[i] - weight[n]))[0][0]
                opt_x1 = profit[n] + tab[row_idx, curr_idx - 1]

                # Selecting the maximum from the selected options.
                if opt_x0 == opt_x1:
                    tab[i, curr_idx] = (0, 1)
                    tab[i, curr_idx + 1] = opt_x0
                elif opt_x1 > opt_x0:
                    tab[i, curr_idx] = 1
                    tab[i, curr_idx + 1] = opt_x1
                else:
                    tab[i, curr_idx] = 0
                    tab[i, curr_idx + 1] = opt_x0
        n -= 1
        curr_idx += 2

    # Print out a decision matrix.
    print_table(y, tab, N)

    # Determination and condensation of results.
    result = extract(0, limit, tab.shape[0]-1, tab.shape[1]-2, y, tab, N, weight)

    # Determination of total profit and weight.
    total_p = result[0] @ np.array(profit)
    total_w = result[0] @ np.array(weight)
    print_result(result, N, ', profit = ' + str(total_p) + ', total_weight = ' + str(total_w))


if __name__ == '__main__':

    # Example
    profit_1 = [1, 3, 2, 2]
    weights_1 = [1, 4, 3, 3]
    knapsack_prob(profit_1, weights_1, 7)
