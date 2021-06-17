import numpy as np
from prettytable import PrettyTable


# Funkcja, która przedstawia macierz decyzji w postaci tabeli.
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


# Funkcja przedstawiająca wszystkie możliwe rozwiązania, w postaci tabeli.
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
Funkcja wyznaczająca wszystkie mozliwe strategie na podstawie uzyskanej macierzy.

Działa w sposób rekurencyjny. Dla każdej decyzji, począwszy od pierwszej sprawdzane
są wszystkie możliwe wybory z listy.
Następnie odpowiednia wartość decyzji zostaje dodana do macierzy wszystkich strategii oraz
następuje rekurencyjne wywołanie funkcji dla odpowiednio wyliczonych parametrów.
Oprócz tego w przypadku gdzie możliwe są dwie różne decyzje, wywoływana jest pętla for,
mająca na celu uzupełnienie końcowej macierzy.
"""

def extract(x, state, row_nr, col_nr, y, tab, N, demand ,lst=None):
    if lst is None:
        lst = [[] for _ in range(N)]

    if x < N:

        if isinstance(tab[row_nr, col_nr], int):
            choice = tab[row_nr, col_nr]
            new_state = state + choice - demand[x]
            new_row_nr = np.where(y == new_state)[0][0]
            lst[x].append(choice)
            extract(x + 1, new_state, new_row_nr, col_nr - 2, y, tab, N, demand, lst)

        else:
            for choice in tab[row_nr, col_nr]:
                new_state = state - choice - demand[x]
                new_row_nr = np.where(y == new_state)[0][0]
                lst[x].append(choice)
                extract(x + 1, new_state, new_row_nr, col_nr - 2, y, tab, N, demand, lst)
                for i in range(len(lst) - 1, 0, -1):
                    while len(lst[i - 1]) < len(lst[i]):
                        lst[i - 1].append(lst[i - 1][-1])
    return list(zip(*lst))


"""
Wyznaczenie optymalnej wielkości partii produkcyjnej.

Zadanie WPP opis zmiennych:
    + time - czas wyrażony w miesiącach,
    + demand - macierz 1xn, wyrażająca wymaganą ilość produktu na dany miesiąc,
    + warehousing - macierz 1xn, określająca koszt składowania danej ilości produktu,
    + cost - koszt produkcji, w zależności od ilości,
    + y_max - maksymalna pojemność magazynu,
    + y_min - minimalna pojemność maganzynu,
    + y_0 - stan magazynu na początku,
    + y_n - stan magazynu na końcu.   
    
Założenia:
    x_n = q_n - y_(n-1)    {  + y_n [Dla ostatniej kolumny]}
    0 <= x_n <= len(cost) - 1
    x_n <= y_max + q_n - y_(n-1)
    x_n >= y_min + q_n - y_(n-1)
    x_n >= q_n - y_(n-1)
"""


# czas całkowity, zapotrzebowanie, zdolność produkcyjna, koszt składowania,
def WPP(time, demand, cost, warehousing, y_min, y_max, y_0, y_n):
    N = time
    n = time - 1
    curr_idx = 0
    x_min = 0
    x_max = len(cost) - 1

    # kolumna y_(i-1) wyrażająca odpowiednie stany.
    y = np.array([i for i in range(y_max + 1)])

    # Utworzenie macierzy, do której będziemy wpisywać wyniki kolejnych operacji.
    tab = np.zeros((len(y), 2 * N), dtype=object)

    # Uzupełninie pierwszej kolumny.
    for i, _ in enumerate(tab[:, curr_idx]):
        x_n = demand[n] - i + y_n
        if (x_min <= x_n <= x_max) and (x_n <= y_max + demand[n] - i) and (x_n >= y_min + demand[n] - i):
            tab[i, 0] = x_n
            tab[i, 1] = cost[x_n] + warehousing[y_n]
        else:
            tab[i, 0] = np.inf
            tab[i, 1] = np.inf

    n -= 1
    curr_idx += 2

    # Uzupełnienie pozostałych kolumn.
    for m in range(N - 1):
        for i, _ in enumerate(tab[:, curr_idx]):

            if m == N - 2 and i != y_0:
                tab[i, curr_idx] = np.inf
                tab[i, curr_idx + 1] = np.inf
                continue

            # Wyznaczenie przedziału wartości dopuszczalnych dla x_i.
            all_costs = []
            x_i = demand[n] - i
            x_i_up = y_max + demand[n] - i
            x_i_down = y_min + demand[n] - i

            all_prod = [j for j in range(x_i_down, x_i_up + 1) if (0 <= j <= x_max)]

            # Znalezienie minimum po koszcie, spośród wszystkich możliwych x_i
            if all_prod:
                for productivity in all_prod:
                    idx = i + productivity - demand[n]
                    all_costs.append( cost[productivity] + warehousing[idx] + tab[idx, curr_idx - 1])

                min_val = np.min(all_costs)
                min_idx = np.where(all_costs == min_val)[0]

                if len(min_idx) > 1:
                    all_x = [all_prod[j] for j in min_idx]
                else:
                    all_x = all_prod[min_idx[0]]

                if min_val == np.inf:
                    all_x = np.inf

                # Jeżeli istnieje więcej niż jedno minimum, to wpisywane jest ono w postaci listy.
                tab[i, curr_idx] = all_x
                tab[i, curr_idx + 1] = min_val

            else:
                tab[i, curr_idx] = np.inf
                tab[i, curr_idx + 1] = np.inf

        n -= 1
        curr_idx += 2

    # Wypisanie macierzy decyzji
    print_table(y, tab, N)

    row_nr = np.where(tab[:, -2] != np.inf)[0][0]

    # Wyznaczenie i wypisanie rezultatu.
    result = extract(0, y_0, row_nr, tab.shape[1] - 2, y, tab, N, demand)
    print_result(result, N, ', cost = ' + str(tab[row_nr, tab.shape[1] - 1]))


if __name__ == '__main__':

    czas = 6
    zapotrzebowanie = [3, 3, 3, 3, 3, 3]
    koszty = [0, 15, 18, 19, 20, 24]
    cena_magazynowania = [0, 0, 4, 6, 10, 12, 18, 24]
    magazyn_min = 0
    magazyn_max = 4
    stan_start = 0
    stan_koniec = 0

    WPP(czas, zapotrzebowanie, koszty, cena_magazynowania, magazyn_min, magazyn_max, stan_start, stan_koniec)
