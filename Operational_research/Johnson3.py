import numpy as np
from prettytable import PrettyTable
import itertools


"""Raised when the basic reduction condition is not met"""
class UnfulfilledConditionError(Exception):
    def __init__(self):
        print("The basic reduction condition is not met")

# Function that allows displaying time matrices in the form of a table.
def print_time_table(time_mat, labels, title=None):
    nlabels = [" "] + labels
    time_table = PrettyTable()
    if title:
        time_table.title = title
    time_table.field_names = nlabels
    for i, row in enumerate(time_mat, 1):
        nrow = [f"M{i}"] + row.tolist()
        time_table.add_row(nrow)
    print("\n")
    print(time_table)
    print("\n")


def print_all_rank_orders(data, title):
    i = 1
    for time_mat, labels in data:
        string = title + f" {i}"
        print_time_table(time_mat, labels, string)
        i += 1

# Johnson algorithm for 3 machines problem.
def Johnson3(time_mat: np.ndarray):
    # Task labels.
    labels = [f"Z{i+1}" for i in range(time_mat.shape[1])]

    # Reduced auxiliary matrix.
    time_p = np.zeros((2, time_mat.shape[1]))

    # Determine the minimum and maximum for each row.
    min_rows = time_mat.min(axis=1)
    max_rows = time_mat.max(axis=1)

    # Checking the Johnson algorithm conditions for 3 machines problem.
    if (min_rows[0] >= max_rows[1]) or (min_rows[2] >= max_rows[1]):
        time_p[0] = time_mat[0] + time_mat[1]
        time_p[1] = time_mat[1] + time_mat[2]
    else:
        raise UnfulfilledConditionError

    # Create auxiliary lists to sort the column indexes accordingly.
    left_part = []
    right_part = []

    print_time_table(time_mat, labels, "Operation time Matrix")
    print_time_table(time_p, labels, "Reduced time Matrix")

    """
    Search for column indexes containing the minimum of the times table and inserting
    them into the appropriate tables, depending on the row number in which they are located.
    If there is more than one minimum in a row, they are inserted into the same list cell as a list
    Finally, the entire columns where the minimum values were located are filled with the np.inf.
    """
    while not np.all(time_p == np.inf):
        min_coord = np.array(np.where(time_p == np.min(time_p)))
        left = []
        right = []
        for i in range(min_coord.shape[1]):
            if min_coord[0, i] == 0:
                col_nr = min_coord[1, i]
                left.append(col_nr)
                time_p[:, col_nr] = np.inf
            else:
                col_nr = min_coord[1, i]
                if time_p[0,col_nr] != np.inf:
                    right += [col_nr]
                    time_p[:, col_nr] = np.inf
        if left:
            left_part.append(left)
        if right:
            right_part.insert(0, right)

    # Combination of segregated indexes.
    complete_idx = left_part + right_part

    """
    Creation of a list, containing lists of acceptable indexes. If the length
    of the internal list is greater than one, it means that in a given place,
    may be a permutation. Therefore, such a list is turned into a permutation list.
    
    Example: complete_idx --> curr_lst
    complete_idx = [[1], [3, 7], [0, 2], [4], [5]]
    curr_lst = [[1], [(3, 7), (7, 3)], [(0, 2), (2, 0)], [4], [5]]
    """

    curr_lst = []
    for indices in complete_idx:
        if len(indices) > 1:
            perm = list(itertools.permutations(indices))
            curr_lst.append(perm)
        else:
            curr_lst.append(indices)

    """
    Create a list of all possible combinations of column indexes.
    Example: curr_lst --> all_combinations
    curr_lst = [[6], [8], [9], [1], [(3, 7), (7, 3)], [(0, 2), (2, 0)], [4], [5]]
    all_combinations = [[6, 8, 9, 1, 3, 7, 0, 2, 4, 5],
                        [6, 8, 9, 1, 3, 7, 2, 0, 4, 5],
                        [6, 8, 9, 1, 7, 3, 0, 2, 4, 5],
                        [6, 8, 9, 1, 7, 3, 2, 0, 4, 5]]
    """

    all_combinations = []
    for comb in itertools.product(*curr_lst):
        temp = []
        for elem in comb:
            if isinstance(elem, tuple):
                temp.extend(elem)
            else:
                temp.append(elem)
        all_combinations.append(temp)


    # Creating a list of matrices of all possible rankings with labels in the form of tuple.

    all_rank_orders = []
    for rank in all_combinations:
        t_labels = []
        t_time_mat = np.zeros_like(time_mat)
        for i, col_num in enumerate(rank):
            t_time_mat[:, i] = time_mat[:, col_num]
            t_labels.append(f"Z{col_num+1}")
        all_rank_orders.append((t_time_mat, t_labels))


    # Calculating the length of the rank order.

    all_rank_orders_len = []

    for rank_order, lab in all_rank_orders:
        rank_len = np.zeros_like(rank_order)
        rank_len[0, 0] = rank_order[0, 0]

        for i in range(1, rank_len.shape[1]):
            rank_len[0, i] = rank_order[0, i] + rank_len[0, i - 1]

        for i in range(1, rank_len.shape[0]):
            rank_len[i, 0] = rank_len[i - 1, 0] + rank_order[i, 0]

        for i in range(1, rank_len.shape[0]):
            for j in range(1, rank_len.shape[1]):
                rank_len[i, j] = max(rank_len[i, j - 1], rank_len[i - 1, j]) + rank_order[i, j]
        all_rank_orders_len.append((rank_len, lab))

    print_all_rank_orders(all_rank_orders, "Final ranking No.")
    print_all_rank_orders(all_rank_orders_len, "Task completion times for ranking No.")

if __name__ == '__main__':
    time_matrix = np.array([[9, 14, 8, 12, 7, 13,  9, 14, 16, 12],
                            [5,  6, 4,  5, 3,  2,  3,  1,  7 , 7],
                            [4,  8, 5,  7, 3,  1, 10, 11, 13, 9]])

    Johnson3(time_matrix)
