import numpy as np


def change_col(graph, numbers):
    graph_c = np.zeros_like(graph)
    for old, new in numbers:
        graph_c[:, new-1] = graph[:, old-1]
    return graph_c


def organized_graph(graph, numbers):
    new_graph = []
    for old, new in numbers:
        new_graph.append(graph[old - 1])
    graph_cpm = change_col(np.array(new_graph), numbers)
    return graph_cpm


def adjmat_to_adjlist(adjmat):
    nb_list = dict()
    for i in range(1, len(adjmat) + 1):
        nb_list[i] = []
    for i, row in enumerate(adjmat, 1):
        for j, nb in enumerate(row, 1):
            if nb != 0:
                nb_list[i].append(j)
    return nb_list


def create_edges(adjmat):
    edges_lst = dict()
    for i, row in enumerate(adjmat, 1):
        for j, nb in enumerate(row, 1):
            if nb != 0:
                edges_lst[(i, j)] = nb
    return edges_lst


class Node:
    def __init__(self):
        self.NWM = 0
        self.NPD = float('inf')
        self.LUZ = None


class CPM:
    def __init__(self, adjmat):
        self.vertices = {i: Node() for i in range(1, len(adjmat) + 1)}
        self.adjlist = adjmat_to_adjlist(adjmat)
        self.edges = create_edges(adjmat)
        self.paths = []
        self.all_paths(list(self.adjlist)[0], list(self.adjlist)[-1])


    def all_paths(self, start, end, visited=None, path=None, track=None):
        if visited is None:
            visited = {u: False for u in self.adjlist}
            path = []
            track = []
        visited[start] = True
        path.append(start)
        if start == end:
            self.paths.append(path[:])
        else:
            for v in self.adjlist[start]:
                if visited[v] is False:
                    self.all_paths(v, end, visited, path, track)
        visited[start] = False
        path.pop()


    def calculate_NWM(self):
        for path in self.paths:
            for i in range(1, len(path)):
                u_p = path[i - 1]
                u = path[i]
                if self.edges[(u_p, u)] < 0:
                    new_nwm = self.vertices[u_p].NWM
                else:
                    new_nwm = self.vertices[u_p].NWM + self.edges[(u_p, u)]
                if self.vertices[u].NWM < new_nwm:
                    self.vertices[u].NWM = new_nwm
        self.vertices[len(self.adjlist)].NPD = self.vertices[len(self.adjlist)].NWM

    def calculate_NPD(self):
        for path in self.paths:
            for i in range(len(path)-2, -1, -1):
                u_p = path[i]
                u = path[i + 1]
                if self.edges[(u_p, u)] < 0:
                    new_npd = self.vertices[u].NPD
                else:
                    new_npd = self.vertices[u].NPD - self.edges[(u_p, u)]
                if self.vertices[u_p].NPD > new_npd:
                    self.vertices[u_p].NPD = new_npd
    def calculate_LUZ(self):
        for vertex in self.vertices:
            self.vertices[vertex].LUZ = self.vertices[vertex].NPD - self.vertices[vertex].NWM

    def find_critical_path(self):
        for path in self.paths:
            if all(self.vertices[vertex].LUZ == 0 for vertex in path):
                return path
        return None

    def show_data(self):
        print("\n========= CPM =========")
        print("{1:<5}{0:^5}{2:>5}".format("NWM", "Nr", "NPD"), f"   LUZ")
        for number, data in self.vertices.items():
            #print(f"Nr: {number}   NWM: {data.NWM}   MPD: {data.NPD}   LUZ: {data.LUZ}")
            print("{1:<5}{0:^5}{2:>5}".format(data.NWM, number, data.NPD),f"   {data.LUZ}")


def number_the_graph(graph):
    new_numbers = [i for i in range(1, len(graph)+1)]
    idx_lst = []
    graph_c = graph.copy()
    size = len(graph)
    while size > 0:
        elem_to_del = []
        for i in range(graph_c.shape[0]):
            if i+1 not in idx_lst:
                if np.all(graph_c[:, i] == 0):
                    size -= 1
                    idx_lst.append(i+1)
                    elem_to_del.append(i)
        for elem in elem_to_del:
            graph_c[:, elem] = 0
            graph_c[elem, :] = 0
    return list(zip(idx_lst, new_numbers))


def run_CPM(graph):
    print("\nstara macierz")
    print(graph)
    print("\n(stary numer, nowy_numer)")
    print(number_the_graph(graph))
    print("\nnowa macierz")
    adjmat = organized_graph(graph, number_the_graph(graph))
    print(adjmat)
    graph_cpm = CPM(adjmat)
    graph_cpm.calculate_NWM()
    graph_cpm.calculate_NPD()
    graph_cpm.calculate_LUZ()
    graph_cpm.show_data()
    print("\nŚcieżka krytyczna")
    print(graph_cpm.find_critical_path())


if __name__ == '__main__':
    x = -1            # 1, 2, 3, 4, 5, 6,  7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
    graphn = np.array([[0, 0, 0, 7, 0, 0,  1, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #1
                       [0, 0, 0, 0, 0, 0,  0, 0, 6, 0,  0,  0,  0,  0,  0,  0,  0], #2
                       [0, 0, 0, 0, 0, 0,  0, 5, 0, 0,  0,  0,  0,  0,  0,  0,  0], #3
                       [0, 0, 0, 0, 0, 12, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #4
                       [0, 0, 0, 0, 0, 16, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #5
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #6
                       [0, 0, 0, 0, x, 0,  0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #7
                       [0, 0, 0, 0, 1, 0,  0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #8
                       [0, 0, 0, 0, 0, 0,  0, 2, 0, 0,  0,  0,  0,  0,  0,  0,  0], #9
                       [0, 4, 0, 0, 0, 0,  0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #10
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0,  0,  7,  0,  0,  5,  0], #11
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 11, 0,  0,  0,  4,  0,  0,  0], #12
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0,  0,  0,  0,  2,  0,  0], #13
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0,  0,  0,  0,  x,  0,  0], #14
                       [9, 0, 3, 0, 0, 0,  0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0], #15
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0,  0,  0,  0,  3,  0,  0], #16
                       [0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  6,  4,  0,  0,  0,  0,  0]]) #17
    run_CPM(graphn)
