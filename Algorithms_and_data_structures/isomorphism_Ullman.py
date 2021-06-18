import numpy as np
import copy
from typing import List, Set
import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, key, data):
        self.key = key
        self.data = data


class Adjacency_matrix:
    def __init__(self):
        self.graph = []
        self.vertices = []

    def order(self):
        return len(self.vertices)

    def search_idx(self, vertex_id):
        for i, v in enumerate(self.vertices):
            if vertex_id == v.key:
                return i
        return None

    def insertVertex(self, data, vertex_id):
        self.vertices.append(Vertex(vertex_id, data))
        if not self.graph:
            self.graph.append([0])
        else:
            self.graph.append([0] * len(self.graph))
            for elem in self.graph:
                elem.append(0)

    def insertEdge(self, vertex1_id, vertex2_id, is_undirected=True):
        idx1 = self.search_idx(vertex1_id)
        idx2 = self.search_idx(vertex2_id)
        if idx1 is None or idx2 is None:
            raise ValueError
        else:
            self.graph[idx1][idx2] = 1
            if is_undirected:
                self.graph[idx2][idx1] = 1

    def deleteVertex(self, vertex_id):
        del_idx = self.search_idx(vertex_id)
        if del_idx is not None:
            del self.vertices[del_idx]
            for elem in self.graph:
                del elem[del_idx]
            del self.graph[del_idx]
        else:
            raise KeyError

    def deleteEdge(self, vertex1_id, vertex2_id, is_undirected=True):
        idx1 = self.search_idx(vertex1_id)
        idx2 = self.search_idx(vertex2_id)
        if idx1 is None or idx2 is None:
            raise ValueError
        else:
            self.graph[idx1][idx2] = 0
            if is_undirected:
                self.graph[idx2][idx1] = 0

    def getVertex(self, vertex_id):
        idx = self.search_idx(vertex_id)
        if idx is None:
            return None
        else:
            return self.vertices[idx]

    def neighbours(self, vertex_id):
        nb_lst = []
        idx = self.search_idx(vertex_id)
        if idx is None:
            raise KeyError
        for i, elem in enumerate(self.graph[idx]):
            if elem == 1:
                nb_lst.append(self.vertices[i].key)
        return nb_lst

    def size(self):
        edges = 0
        for row in self.graph:
            for elem in row:
                if elem == 1:
                    edges += 1
        return edges

    def edges(self):
        lst_of_edges = []
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                if self.graph[i][j] == 1:
                    lst_of_edges.append((self.vertices[i].key, self.vertices[j].key))
        return lst_of_edges

    def keys_tuples(self):
        lst = []
        for vertex in self.vertices:
            lst.append((vertex.key, vertex.key))
        return lst

    def _choose_color(self, vertex_id, set_colors, idx):
        occupied = set()
        nb = self.neighbours(vertex_id)
        for nr, row in enumerate(self.graph):
            if row[idx] == 1 and nr not in nb:
                nb.append(self.vertices[nr].key)
        col = 0
        for elem in set_colors:
            if elem[0] in nb:
                occupied.add(elem[1])
        for elem in occupied:
            if elem == col:
                col += 1
            else:
                break
        return vertex_id, col

    def color_graph(self, vertex_id):
        colors = {0: 'white', 1: 'red', 2: 'blue', 3: 'green', 4: 'yellow', 5: 'brown', 6: 'black'}
        colored_v = []
        stack = [vertex_id]
        set_colors = []
        visited = []
        while stack:
            vertex_id = stack.pop()
            if vertex_id not in visited:
                visited.append(vertex_id)
                idx = self.search_idx(vertex_id)
                set_colors.append(self._choose_color(vertex_id, set_colors, idx))
                for i in range(len(self.graph[idx]) - 1, -1, -1):
                    stack.append(self.vertices[i].key)
        for elem in set_colors:
            colored_v.append((elem[0], colors[elem[1]]))
        return colored_v

    def create_connection(self, data):
        v1, v2, weight = data

        node1 = self.getVertex(v1)
        node2 = self.getVertex(v2)

        if node1 is None:
            self.insertVertex(v1, v1)
        if node2 is None:
            self.insertVertex(v2, v2)

        self.insertEdge(v1, v2)

    def get_adjMatrix(self):
        return np.array(self.graph)


def get_nb_num(adjmatrix, v_idx):
    total_nb = 0
    for elem in adjmatrix[v_idx]:
        if elem != 0:
            total_nb += 1
    return total_nb

def get_nb_lst(adjmatrix, v_idx):
    nb_lst = []
    for i, elem in enumerate(adjmatrix[v_idx]):
        if elem != 0:
            nb_lst.append(i)
    return nb_lst

def M0_condition(cur_row, col, G, P):
    G_nb = get_nb_num(G, col)
    P_nb = get_nb_num(P, cur_row)
    if G_nb < P_nb:
        return False
    return True

def is_isomorphism(G, P, M):
    if (P == M @ (M @ G).T).all():
        return True
    return False



def Ullman_1(used_col: Set, curr_row: int, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0):

    if curr_row == M.shape[0]:
        if is_isomorphism(G, P, M):
            print(M)
            print(" ")
        return no_recursion
    Mc = M.copy()

    unused_col = {i for i in range(M.shape[1]) if i not in used_col}

    for c in unused_col:
        Mc[curr_row, c] = 1
        Mc[curr_row, :c] = 0
        Mc[curr_row, c + 1:] = 0
        used_col.add(c)
        no_recursion = Ullman_1(used_col, curr_row + 1, G, P, Mc, no_recursion + 1)
        used_col.remove(c)
    return no_recursion



def Ullman_2(used_col: Set, curr_row: int, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0):

    if curr_row == M.shape[0]:
        if is_isomorphism(G, P, M):
            print(M)
            print(" ")
        return no_recursion
    Mc = M.copy()

    unused_col = {i for i in range(M.shape[1]) if i not in used_col}

    for c in unused_col:
        if M0_condition(curr_row, c, G, P):
            Mc[curr_row, c] = 1
            Mc[curr_row, :c] = 0
            Mc[curr_row, c + 1:] = 0
            used_col.add(c)
            no_recursion = Ullman_2(used_col, curr_row + 1, G, P, Mc, no_recursion + 1)
            used_col.remove(c)
    return no_recursion



def Ullman_3(used_col: Set, curr_row: int, G: np.ndarray, P: np.ndarray, M: np.ndarray, no_recursion=0):

    if curr_row == M.shape[0]:
        if is_isomorphism(G, P, M):
            print(M)
            print(" ")
        return no_recursion

    Mc = M.copy()

    unused_col = {i for i in range(M.shape[1]) if i not in used_col}

    for c in unused_col:
        if M0_condition(curr_row, c, G, P):
            Mc[curr_row, c] = 1
            Mc[curr_row, :c] = 0
            Mc[curr_row, c + 1:] = 0
            switch = True
            if curr_row == Mc.shape[0] - 1:
                Mp = prune(Mc, G, P)
                if np.any(np.max(Mp, axis=1) == 0):
                    switch = False
            if switch:
                used_col.add(c)
                no_recursion = Ullman_3(used_col, curr_row + 1, G, P, Mc, no_recursion + 1)
                used_col.remove(c)
    return no_recursion


def prune(M: np.ndarray, G, P):
    M = M.copy()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == 1:
                G_nb = get_nb_lst(G, j)
                P_nb = get_nb_lst(P, i)
                for x in P_nb:
                    for y in G_nb:
                        if M[x, y] == 1:
                            break
                    else:
                        M[i, j] = 0
                        return M
    return M


if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt

    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1), ('F', 'A', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1), ('C', 'D', 1)]

    graph_g = Adjacency_matrix()
    graph_p = Adjacency_matrix()

    for edge_g in graph_G:
        graph_g.create_connection(edge_g)

    for edge_p in graph_P:
        graph_p.create_connection(edge_p)

    adj_mat_g = graph_g.get_adjMatrix()
    adj_mat_p = graph_p.get_adjMatrix()
    mat = np.zeros((adj_mat_p.shape[0], adj_mat_g.shape[0]))

    print("-"*20)
    print("~~ Macierze M:")
    print("-" * 20)
    result1 = Ullman_1(set(), 0, adj_mat_g, adj_mat_p, mat)

    print("-"*20)
    print("~~ Macierze M:")
    print("-" * 20)
    result2 = Ullman_2(set(), 0, adj_mat_g, adj_mat_p, mat)

    print("-"*20)
    print("~~ Macierze M:")
    print("-" * 20)
    result3 = Ullman_3(set(), 0, adj_mat_g, adj_mat_p, mat)

    print("Ullman_1, no_recursion  = ", result1)
    print("Ullman_2, no_recursion  = ", result2)
    print("Ullman_3, no_recursion  = ", result3)

    # # Rysowanie grafów

    # G = nx.Graph()
    # for v1, v2, w in graph_P:
    #     G.add_edge(v1, v2, weight=w)

    # """ draw graph G """
    # layout = nx.spring_layout(G)
    # nx.draw(G, layout, node_size=1000, with_labels=True, font_weight='bold', font_size=15)
    # labels = nx.get_edge_attributes(G,'weight')
    # nx.draw_networkx_edge_labels(G,pos=layout,edge_labels=labels)
    # plt.show()
    #
    # G2 = nx.Graph()
    # for v1, v2, w in graph_G:
    #     G2.add_edge(v1, v2, weight=w)
    #
    # """ draw graph G """
    # layout = nx.spring_layout(G2)
    # nx.draw(G2, layout, node_size=1000, with_labels=True, font_weight='bold', font_size=15)
    # labels = nx.get_edge_attributes(G2,'weight')
    # nx.draw_networkx_edge_labels(G2,pos=layout,edge_labels=labels)
    # plt.show()
