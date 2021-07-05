from typing import List, Dict, Tuple, Union
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# funkcja tworząca drogę do wybranego wierzchołka
def extract_path(v, previous, visited=None):    # v-wierzchołek, previous-słownik z poprzednikami
    if visited is None:
        visited = []    # stworzenie listy pomocniczej
    if previous[v] is None: # jeżeli wierzchołek nie ma poprzednika
        visited = [v] + visited # dodaj go do listy
        return visited  # zwróć drogę pokonaną od wierzchołka początkowego do wierzchołka v
    else:   # jeżeli ma poprzednika
        visited = [v] + visited     # dodajemy go do ścieżki
        return extract_path(previous[v], previous, visited) # badamy dalej poprzednie wierzchołki

# funkcja zwracająca listę wszystkich ścieżek
def all_paths(previous: Dict[int, int]):
    paths = dict()  # stworzenie słownika dróg
    for u in previous:  # dla każdego wierzchołka który ma poprzednika
        paths[u] = (extract_path(u, previous))  # wywołanie funkcji w celu uzyskania drogi
    return paths

# algorytm Bellmana Forda: jako argumenty BellmanFord(graf w postaci ziobru krawędzi z wagami, wierzchołek początkowy)
def BellmanFord(graph: nx.Graph, s: int) -> Tuple[Dict[int, Union[int, float]], Dict[int, List[int]]]:
    is_directed = nx.is_directed(graph) # sprawdzenie czy graf jest skierowany
    d = dict()  # stworzenie słowników: d-[wierzchołek, koszt], p-[wierzchołek, poprzednik]
    p = dict()
    for u in graph: # dla każdego wierzchołka w grafie nadajemy wartości początkowe
        d[u] = float('inf')
        p[u] = None
    d[s] = 0    # dystans s ustawiamy na 0, ponieważ z niego startujemy
    for i in range(len(graph) - 1): # dokonujemy relaksacji V - 1 razy dla każdej krawędzi
        for u, v, w in graph.edges(data=True):  # dla każdej krawędzi (u, v) i wagi "w" w grafie
            if d[u] != float('inf') and d[u] + w['weight'] < d[v]:  # jeżeli koszt dotarcia z s do "u" (d[u])
                # nie jest wartością początkową i  suma (d[u] i kosztu dotarcia z u do v) jest mniejsza od kosztu
                # dotarcia z s do wierzchołka v, to:
                d[v] = d[u] + w['weight']   # dodajemy koszt drogi z "u" do :v:
                p[v] = u    # ustawiamy poprzednika wierzchołka "v" na "u"
            if not is_directed: # ze względu na to że w gdy graf jest nieskierowany i po nim iterujemy, otrzymujemy
                # tylko jednostronne połączenia, to uwzględniam połączenie z drugiej strony
                if d[v] != float('inf') and d[v] + w['weight'] < d[u]:
                    d[u] = d[v] + w['weight']
                    p[u] = v

    # sprawdzenie czy graf nie posiada ujemnego cyklu. W powyższej części otrzymaliśmy najkrótsze ścieżki, o ile graf
    # nie zawiera ujemnych cykli. Jeżeli w poniższej części znajdziemy krótszą ścieżkę, to oznacza że w grafie występuje
    # cykl ujemny.
    for u, v, w in graph.edges(data=True):
        if d[u] != float('inf') and d[u] + w['weight'] < d[v]:
            raise Exception(f'wykryto ujemny cykl')
        if not is_directed: # uwzględnienie drugiego połączenia w grafie nieskierowanym
            if d[v] != float('inf') and d[v] + w['weight'] < d[u]:
                raise Exception(f'wykryto ujemny cykl')
    v_to_del = []   # stworzenie listy wierzchołków do usunięcia
    for vertex in d:    # dla każdego wierzchołka w grafie
        if d[vertex] == float('inf'):   # jeżeli koszt dotarcia do niego, jest równy wartości startowej
            v_to_del.append(vertex) # to dodajemy go do listy
    for vertex in v_to_del: # iteryjemy po elementach listy v_to_del
        del d[vertex]   # usuwamy ze słownika kosztów, wierzchołki do których nie da się dotrzeć
        del p[vertex]   # usuwamy ze słownika poprzedników, wierzchołek nie posiadający żadnych poprzedników
    paths = all_paths(p)    # tworzymy kompletną ścieżkę dotarcia do danego wierzchołka z wierzchołka początkowego
    return d, paths # zwracamy słownik kosztów oraz listę ścieżek


""""" Graf 1 spójny pojedyncze krawędzie nieskierowany"""""

G = nx.Graph()
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=3)
G.add_edge(1, 4, weight=2)
G.add_edge(2, 5, weight=1)
G.add_edge(3, 5, weight=2)
G.add_edge(3, 6, weight=1)
G.add_edge(4, 6, weight=3)
G.add_edge(4, 7, weight=4)
G.add_edge(5, 6, weight=1)
G.add_edge(5, 10, weight=2)
G.add_edge(5, 8, weight=3)
G.add_edge(8, 9, weight=1)


""""" graf skierowany z ujemnymi wagami """

g1 = nx.DiGraph()
g1.add_weighted_edges_from([(1, 2, -1)])
g1.add_weighted_edges_from([(3, 1, 4)])
g1.add_weighted_edges_from([(2, 3, 3)])
g1.add_weighted_edges_from([(2, 4, 1)])
g1.add_weighted_edges_from([(5, 2, 2)])
g1.add_weighted_edges_from([(4, 3, 5)])
g1.add_weighted_edges_from([(5, 4, 3)])
g1.add_weighted_edges_from([(3, 6, 2)])
g1.add_weighted_edges_from([(6, 4, -1)])
g1.add_weighted_edges_from([(7, 5, -1)])
g1.add_weighted_edges_from([(8, 7, 3)])
g1.add_weighted_edges_from([(4, 8, 4)])
g1.add_weighted_edges_from([(5, 9, -2)])
g1.add_weighted_edges_from([(9, 8, 5)])
g1.add_weighted_edges_from([(10, 9, 3)])

""""" graf skierowany z ujemnymi wagami (ujemny cykl) """

g2 = nx.DiGraph()
g2.add_weighted_edges_from([(1, 2, -1)])
g2.add_weighted_edges_from([(3, 1, 4)])
g2.add_weighted_edges_from([(2, 3, 3)])
g2.add_weighted_edges_from([(2, 4, -1)])
g2.add_weighted_edges_from([(5, 2, 2)])
g2.add_weighted_edges_from([(4, 3, 5)])
g2.add_weighted_edges_from([(4, 5, -3)])
g2.add_weighted_edges_from([(3, 6, 2)])
g2.add_weighted_edges_from([(6, 4, -1)])
g2.add_weighted_edges_from([(7, 5, -1)])
g2.add_weighted_edges_from([(8, 7, 3)])
g2.add_weighted_edges_from([(4, 8, 4)])
g2.add_weighted_edges_from([(5, 9, -2)])
g2.add_weighted_edges_from([(9, 8, 5)])
g2.add_weighted_edges_from([(10, 9, 3)])

try:
    x, y = BellmanFord(G, 1)
    print("\nDla grafu G nieskierowanego, wagi dodatnie")
    print(x)
    print(y)
except Exception as error:
    print(error, "w grafie G")

try:
    x, y = BellmanFord(g1, 8)
    print("\nDla grafu g1 skierowanego, wagi ujemne")
    print(x)
    print(y)
except Exception as error:
    print(error, "w grafie g1")

try:
    x, y = BellmanFord(g2, 7)
    print("Dla grafu g2 skierowanego, cykl ujemny")
    print(x)
    print(y)
except Exception as error:
    print("\nDla grafu g2 skierowanego, cykl ujemny")
    print(error, "w grafie g2")



""""" graf skierowany """

g = nx.DiGraph()
g.add_weighted_edges_from([(1, 2, 1)])
g.add_weighted_edges_from([(3, 1, 4)])
g.add_weighted_edges_from([(2, 3, 3)])
g.add_weighted_edges_from([(2, 4, 1)])
g.add_weighted_edges_from([(5, 2, 2)])
g.add_weighted_edges_from([(4, 3, 5)])
g.add_weighted_edges_from([(5, 4, 3)])
g.add_weighted_edges_from([(3, 6, 2)])
g.add_weighted_edges_from([(6, 4, 1)])
g.add_weighted_edges_from([(7, 5, 1)])
g.add_weighted_edges_from([(8, 7, 3)])
g.add_weighted_edges_from([(4, 8, 4)])
g.add_weighted_edges_from([(5, 9, 2)])
g.add_weighted_edges_from([(9, 8, 5)])
g.add_weighted_edges_from([(10, 9, 3)])

""" draw graph G """
# layout = nx.spring_layout(G)
# nx.draw(G, layout, node_size=1000, with_labels=True, font_weight='bold',  font_size=15)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G,pos=layout,edge_labels=labels)
# plt.show()

""" draw graph g1 """
# layout = nx.circular_layout(g1)
# nx.draw(g1, layout, node_size=900, with_labels=True, font_weight='bold',   font_size=15)
# labels = nx.get_edge_attributes(g1,'weight')
# nx.draw_networkx_edge_labels(g1,pos=layout,edge_labels=labels)
# plt.show()

""" draw graph g2 """
# layout = nx.circular_layout(g2)
# nx.draw(g2, layout, node_size=1000, with_labels=True, font_weight='bold', font_size=15)
# labels = nx.get_edge_attributes(g2,'weight')
# nx.draw_networkx_edge_labels(g2,pos=layout,edge_labels=labels)
# plt.show()
