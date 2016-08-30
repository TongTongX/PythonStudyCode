# CMPUT275 A2 - Assignment 1: Part 1
# Created by Zichun Lin & Zhenzhe Xu on 2016/01/24


from math import sqrt

class Graph:
    '''A graph has a set of vertices and a set of edges, with each edge
    being an ordered pair of vertices.
    '''

    def __init__ (self):
        self._alist = {}
        self.edgeName = {}
    
    def add_vertex (self, vertex):
        ''' Adds 'vertex' to the graph
        Preconditions: None
        Postconditions: self.is_vertex(vertex) -> True
        '''
        if vertex not in self._alist:
            self._alist[vertex] = set()

    def add_edge (self, source, destination):
        ''' Adds the edge (source, destination)
        Preconditions: None
        Postconditions:
        self.is_vertex(source) -> True,
        self.is_vertex(destination),
        self.is_edge(source, destination) -> True
        '''
        self.add_vertex(source)
        self.add_vertex(destination)
        self._alist[source].add(destination)

    def is_edge (self, source, destination):
        '''Checks whether (source, destination) is an edge
        '''
        return (self.is_vertex(source)
                and destination in self._alist[source])

    def is_vertex (self, vertex):
        '''Checks whether vertex is in the graph.
        '''
        return vertex in self._alist

    def neighbours (self, vertex):
        '''Returns the set of neighbours of vertex. DO NOT MUTATE
        THIS SET.
        Precondition: self.is_vertex(vertex) -> True
        '''
        return self._alist[vertex]

    def vertices(self):
        return set(self._alist.keys())


    # ------------------- Add more properties for assignment 1--------------------------
    def add_edgeName(self, source, destination, edgeName):
        self.edgeName[(source, destination)] = edgeName

    # ------------- Add more properties for assignment 1 ends --------------------


class UndirectedGraph(Graph):
    def add_edge(self, a, b):
        super().add_edge(a, b)
        super().add_edge(b, a)

class WeightedGraph(Graph):
        def add_vertex (self, vertex):
            if vertex not in self._alist:
                self._alist[vertex] = {}

        def add_edge (self, source, destination, weight=None):
            self.add_vertex(source)
            self.add_vertex(destination)
            self._alist[source][destination] = weight

        def neighbours(self, vertex):
            return self._alist[vertex].keys()
