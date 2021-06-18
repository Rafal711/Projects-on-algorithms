import random


class Union_Find:
    def __init__(self, size):
        self.parent = [i for i in range(size)]
        self.size = [i for i in range(size)]
        self.n = size

    def find(self, v):
        if self.parent[v] == v:
            return v
        return self.find(self.parent[v])

    def same_component(self, v, w):
        root_v = self.find(v)
        root_w = self.find(w)
        if root_v == root_w:
            return True
        return False

    def merge_component(self, v, w):
        root_v = self.find(v)
        root_w = self.find(w)
        if root_v != root_w:
            if self.size[root_v] > self.size[root_w]:
                if self.size[root_v] - self.size[v] > 3:
                    self.parent[root_w] = root_v
                    self.size[root_v] += self.size[root_w]
                else:
                    self.parent[root_w] = v
                    self.size[v] += self.size[root_w]
            else:
                if self.size[root_w] - self.size[w] > 3:
                    self.parent[root_v] = root_w
                    self.size[root_w] += self.size[root_v]
                else:
                    self.parent[root_v] = w
                    self.size[w] += self.size[root_v]


class Vertex:
    def __init__(self, key, data, color):
        self.key = key
        self.data = data
        self.color = color

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Adjacency_list:
    def __init__(self):
        self.graph = dict()
        self.weights = dict()

    def getVertex(self, vertex_id):
        for v in self.graph:
            if v.key == vertex_id:
                return v
        return None

    def insertVertex(self, vertex_id, color=None, data=None):
        self.graph[Vertex(vertex_id, data, color)] = []

    def insertEdge(self, vertex1_id, vertex2_id, weight, is_undirected=True):
        node1 = self.getVertex(vertex1_id)
        node2 = self.getVertex(vertex2_id)
        if node1 is None or node2 is None:
            raise ValueError
        self.graph[node1].append(vertex2_id)
        self.weights[(vertex1_id, vertex2_id)] = weight
        if is_undirected:
            self.graph[node2].append(vertex1_id)
            self.weights[(vertex2_id, vertex1_id)] = weight

    def create_connection(self, data):
        vertex1_id, vertex2_id, weight = data
        vertex1_ptr = self.getVertex(vertex1_id)
        vertex2_ptr = self.getVertex(vertex2_id)
        if vertex1_ptr is None:
            self.insertVertex(vertex1_id)
        if vertex2_ptr is None:
            self.insertVertex(vertex2_id)
        self.insertEdge(vertex1_id, vertex2_id, weight)

    def deleteVertex(self, vertex_id):
        node = self.getVertex(vertex_id)
        if node is None:
            raise KeyError
        for node_nr in self.graph[node]:
            del self.weights[(node.key, node_nr)]
            del self.weights[(node_nr, node.key)]
        del self.graph[node]
        for val in self.graph.values():
            if vertex_id in val:
                val.remove(vertex_id)

    def deleteEdge(self, vertex1_id, vertex2_id, is_undirected=True):
        node1 = self.getVertex(vertex1_id)
        node2 = self.getVertex(vertex2_id)
        if node1 is None or node2 is None:
            raise KeyError
        self.graph[node1].remove(vertex2_id)
        del self.weights[(vertex1_id, vertex2_id)]
        if is_undirected:
            self.graph[node2].remove(vertex1_id)
            del self.weights[(vertex2_id, vertex1_id)]

    def neighbours(self, vertex_id):
        node = self.getVertex(vertex_id)
        if node is None:
            raise KeyError
        return self.graph[node]

    def set_color(self, vertex_id, color):
        node = self.getVertex(vertex_id)
        node.set_color(color)

    def get_color(self, vertex_id):
        node = self.getVertex(vertex_id)
        return node.get_color()

    def order(self):
        return len(self.graph)

    def size(self):
        gsize = 0
        for val in self.graph.values():
            gsize += len(val)
        return gsize

    def edges(self):
        lst_of_edges = []
        for keys, nb in self.graph.items():
            for u in nb:
                lst_of_edges.append((keys.key, u))
        return lst_of_edges

    def vertex_edges(self, vertex_id):
        node = self.getVertex(vertex_id)
        lst_of_edges = []
        for node_nr in self.graph[node]:
            lst_of_edges.append((vertex_id, node_nr))
        return lst_of_edges

    def keys_tuples(self):
        lst = []
        for vertex in self.graph:
            lst.append((vertex.key, vertex.key))
        return lst

    def _choose_color(self, node, set_colors):
        occupied = set()
        nb = self.graph[node]
        for vertex, val in self.graph.items():
            if node.key in val and vertex.key not in nb:
                nb.append(vertex.key)
        col = 0
        for elem in set_colors:
            if elem[0] in nb:
                occupied.add(elem[1])
        for elem in occupied:
            if elem == col:
                col += 1
            else:
                break
        return node.key, col

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
                node = self.getVertex(vertex_id)
                set_colors.append(self._choose_color(node, set_colors))
                for i in range(len(self.graph[node]) - 1, -1, -1):
                    stack.append(self.graph[node][i])
        for elem in set_colors:
            colored_v.append((elem[0], colors[elem[1]]))
        return colored_v

    def prim_mst(self):
        start = random.choice(list(self.graph.keys()))
        n = len(self.graph)
        labels = [elem for elem in self.graph]
        total_dist = 0

        intree = [0 for _ in range(n)]
        distance = [float('inf') for _ in range(n)]
        parent = [-1 for _ in range(n)]

        T_prim = Adjacency_list()
        for vertex in self.graph:
            T_prim.insertVertex(vertex.key, vertex.color, vertex.data)

        v: Vertex = start
        v_idx = labels.index(v)
        distance[v_idx] = 0

        while intree[labels.index(v)] == 0:
            v_idx = labels.index(v)
            intree[v_idx] = 1
            for u in self.graph[v]:
                u_idx = labels.index(self.getVertex(u))
                if intree[u_idx] == 0:
                    if self.weights[(v.key, u)] < distance[u_idx]:
                        distance[u_idx] = self.weights[(v.key, u)]
                        parent[u_idx] = v.key
            not_visited_dist_label = []
            for vertex in self.graph:
                vertex_idx = labels.index(vertex)
                if intree[vertex_idx] == 0:
                    not_visited_dist_label.append((distance[vertex_idx], vertex_idx))
            if not_visited_dist_label:
                min_val = min(not_visited_dist_label)
                min_idx = min_val[1]
                v = labels[min_idx]
                T_prim.insertEdge(parent[min_idx], v.key, self.weights[(parent[min_idx], v.key)])
                total_dist += self.weights[(parent[min_idx], v.key)]
        return T_prim

    def Kruskal(self):
        key2label = lambda key: ord(key) - 65
        label2key = lambda label: chr(label + 65)

        T_kruskal = Adjacency_list()
        for vertex in self.graph:
            T_kruskal.insertVertex(vertex.key)
        union_find = Union_Find(self.order())

        sorted_edges = [(key, value) for (key, value) in sorted(self.weights.items(), key=lambda x: x[1], reverse=True)]
        n = self.order()
        counter = 0

        while counter < n - 1:
            ((v, w), weight) = sorted_edges.pop()
            if not union_find.same_component(key2label(v), key2label(w)):
                T_kruskal.insertEdge(v, w, weight)
                union_find.merge_component(key2label(v), key2label(w))
                counter += 1
        return T_kruskal


if __name__ == '__main__':
    graf = [('A', 'B', 4), ('A', 'C', 1), ('A', 'D', 4),
            ('B', 'E', 9), ('B', 'F', 9), ('B', 'G', 7), ('B', 'C', 5),
            ('C', 'G', 9), ('C', 'D', 3),
            ('D', 'G', 10), ('D', 'J', 18),
            ('E', 'I', 6), ('E', 'H', 4), ('E', 'F', 2),
            ('F', 'H', 2), ('F', 'G', 8),
            ('G', 'H', 9), ('G', 'J', 8),
            ('H', 'I', 3), ('H', 'J', 9),
            ('I', 'J', 9)
            ]

    graph = Adjacency_list()
    for conntection in graf:
        graph.create_connection(conntection)
    print("MST Kruskal edges:")
    kruskal = graph.Kruskal()
    print(kruskal.edges())
