# -*- coding: utf-8 -*-
from collections import defaultdict, deque

from .graph import UndirectedWeightedGraph as Graph
from .priorityqueue import PriorityQueue
from .algorithms import shortest_path_dijkstra as dijkstra
from .algorithms import prim, kruskal


def shortest_path(graph, start, terminals):

    dist, prev = dijkstra(graph,start)

    distancias = defaultdict(dict)
    distancias[start] = dist

    previos = defaultdict(dict)
    previos[start] = prev

    pqueue = PriorityQueue()

    for t in terminals:
        pqueue.push(distancias[start][t], (start,t))

    subtree = Graph()

    while pqueue:
        source, target = pqueue.pop()
        t = target

        if target not in distancias:
                dist, prev = dijkstra(graph,target)
                distancias[target] = dist
                previos[target] = prev
                for tmp in terminals:
                    pqueue.push(distancias[target][tmp], (target,tmp))

        if target not in subtree.vertices :
            while distancias[source][t]:
                u = previos[source][t]
                w = graph[u][t]
                subtree.add_edge(t,u,weight=w)
                t = u

                if u not in distancias:
                    dist, prev = dijkstra(graph,u)
                    distancias[u] = dist
                    previos[u] = prev
                    for tmp in terminals:
                        pqueue.push(distancias[u][tmp], (u,tmp))

    gg, custo = prunning_mst(subtree, start, terminals)

    return gg, custo


def shortest_path_with_origin(graph, start, terminals):
    '''
    Adaptação para o algortimo Shortest Path with Origin Heuristic

    A Árvore solução Tspoh é contruida iterativamente: um vertice terminal é incluido por vez.

    Determina-se a árvore de caminhos mínimos de um ponto inicial <start> até os demais vértices;
    A partir de cada vértice terminal incluí-se o menor caminho até <start>
    Um vértice terminal ou está nas folhas da árvore formada, ou está no caminho de outro nó terminal.
    '''

    dist, prev = dijkstra(graph,start)
    custo = 0

    stree = Graph()

    for u in terminals:
        while dist[u] :
            v = prev[u]
            if not stree.has_edge(u,v):
                w = graph[u][v]
                stree.add_edge(u,v,weight=w)
                custo += w
            else:
                break
            u = v

    return stree, custo


def shortest_path_origin_prim(graph, start, terminals):
    '''
    Determinar a árvore de caminhos mínimos <T> dos vértices terminais até o nó <start>
    Define um subgrafo formado pelos vértices presentes em T
    com as correspondentes arestas do grafo G <graph>.
    Calcula a MST do subgrafo considerado e realiza a poda da MST.
    '''

    dist, prev = dijkstra(graph, start)

    selectedNodes = set([start])

    for t in terminals:
        selectedNodes.add(t)
        u = t
        while dist[u]:
            v = prev[u]
            selectedNodes.add(v)
            u = v

    subgraph = Graph()

    for v in selectedNodes:
        for u in graph.adjacent_to(v):
            if (u in selectedNodes):
                w = graph.edges[v][u]
                subgraph.add_edge(v, u, weight=w)

    subtree, cost = prunning_mst(subgraph, start, terminals)

    return subtree, cost


def prunning_mst(graph, start, terminals):
    '''
    Parameters:
        graph : Graph
            Base graph to compute the Steiner tree
        start : Node
            Where is to start Prim's algorithm
        terminals : Set
            Terminals Nodes from the STPG instance

    Return:
        prunning : A Steiner Tree
        total : Numeric - total cost of the tree

    Notes:
        Determina a MST do grafo por meio do algoritmo de Prim.
        Realiza a poda considerando os nós terminais como os nós folhas até a raiz <start>
        Se <start> for um vértice não terminal, o laço <while> verifica se <start> é um vértice folha da árvore resultande.
        Em caso afirmativo realiza uma poda iterativa a partir desse vértice para garantir que a árvore resultante seja
        uma árvore de Steiner.
        Resulta sempre na mesma árvore para qualquer vértice <start> considerado.
    '''
    dict_tree, _ = prim(graph, start)

    prunning = Graph()

    total = 0

    for terminal in terminals:
        current = terminal
        while current != start:
            previous = dict_tree[current]
            if prunning.has_edge(current, previous):
                current = start
            else :
                weight = graph.weight(current, previous)
                prunning.add_edge(current, previous, weight=weight)
                total += weight
                current = previous

    current = start
    while (current not in terminals) and (prunning.degree(current) == 1):
        previous = list(prunning.adjacent_to(current)).pop()
        total -= prunning.weight(current, previous)
        prunning.remove_node(current)
        current = previous

    return prunning, total


def prunning_kruskal_mst(graph : Graph, terminals):
    """
    Parameters:
        graph : Graph
        terminals : list of nodes

    Return:
        child : Graph
            Steiner Tree
    """
    child = kruskal(graph)

    fifo = deque([v for v in child.vertices if (v not in terminals) and (child.degree(v) == 1)])

    while fifo:
        v = fifo.pop()
        for w in child.adjacent_to(v):
            if (w not in terminals) and (child.degree(w) == 2): # or child.degree(w) - 1 == 1 #
                fifo.appendleft(w)

        child.remove_node(v)

    return child
