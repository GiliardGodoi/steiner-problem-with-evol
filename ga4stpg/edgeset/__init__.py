
class GEdge:
    '''General Edge Abrastraction'''
    def __init__(self, v, w, weight=None):
        self._edge = (v, w)

        if weight :
            self._weight = weight

    def __str__(self):
        return f"Edge <{self._edge}>"

    def __repr__(self):
        return f"Edge <{self._edge}>"

    def __hash__(self):
        return hash(self._edge)

    def __contains__(self, vertice):
        return vertice in self._edge

    def __iter__(self):
        return iter(self._edge)

    def __getitem__(self, key):
        return self._edge[key]

    def __len__(self):
        return self._weight

    def __eq__(self, other):
        return self._edge == other._edge

    @property
    def vertices(self):
        for v in self._edge:
            yield v


class UEdge(GEdge):
    '''Undirected Edge
    The edges below are suppose to be equal
        Edge<4, 5> == Edge <5, 4>
    '''
    def __init__(self, v, u, **kwargs):
        super().__init__(min(u,v), max(u, v), **kwargs)


class DEdge(GEdge):
    '''Directed Edge'''
    def __init__(self, v, u, **kwargs):
        super().__init__(v, u, **kwargs)


class EdgeSet:

    def __init__(self,items=None):
        self._edges = set()

        if items and isinstance(items, (list, tuple, set)):
            for item in items:
                u, v = item
                self._edges.add(UEdge(v,u))
        elif items and isinstance(items, self.__class__):
            self._edges = items._edges.copy()

    def __str__(self):
        return f'EdgeSet: <{len(self)}>'

    def __repr__(self):
        return f'EdgeSet: <{len(self)}>'

    def __contains__(self, item):
        return item in self._edges

    def __iter__(self):
        return iter(self._edges)

    def __len__(self):
        return len(self._edges)

    def __sub__(self, other):
        '''- operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for -: '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges - other._edges)

    def __and__(self, other):
        '''& operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for &: '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges & other._edges)

    def __xor__(self, other):
        '''^ operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for ^: '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges ^ other._edges)

    def __or__(self, other):
        ''' | operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for -: '{type(self)}' and {type(other)}")
        return EdgeSet(self._edges | other._edges)

    def __eq__(self, other):
        '''== operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for ==: '{type(self)}' and {type(other)}")
        return self._edges == other._edges

    def __lt__(self, other):
        '''< operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for < '{type(self)}' and {type(other)}")
        return self._edges < other._edges

    def __le__(self, other):
        '''<= operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) <=  for '{type(self)}' and {type(other)}")
        return self._edges <= other._edges

    def __gt__(self, other):
        '''> operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) > for '{type(self)}' and {type(other)}")
        return self._edges > other._edges

    def __ge__(self, other):
        '''>= operator '''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) >= for '{type(self)}' and {type(other)}")
        return self._edges >= other._edges

    @property
    def vertices(self):
        done = set()
        for edge in self._edges:
            for vertice in edge:
                if vertice not in done:
                    done.add(vertice)
                    yield vertice

    def add(self, *args):
        u, v = None, None

        if len(args) == 1:
            item = args[0]
        elif len(args) == 2:
            u, v = args
            item = UEdge(u, v)
        else:
            item = None

        if isinstance(item, UEdge):
            self._edges.add(item)
            return
        elif isinstance(item, (list, tuple)) and len(item) == 2 :
            u, v = item
        elif isinstance(item, list) and len(item) == 1 and len(item[0]) == 2:
            u, v = item[0]
        elif isinstance(item, set) and len(item) == 2:
            u = item.pop()
            v = item.pop()
        else:
            raise ValueError(f"could not understand input f{item}")

        edge = UEdge(u, v)

        self._edges.add(edge)

    def discard(self, edge):
        if not isinstance(edge, UEdge):
            u, v = edge
            edge = UEdge(u, v)
        self._edges.discard(edge)

    def remove(self, edge):
        if not isinstance(edge, UEdge):
            u, v = edge
            edge = UEdge(u, v)
        self._edges.remove(edge)

    def issubset(self, other):
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported method for'{type(self)}' and {type(other)}")
        return self._edges.issubset(other._edges)

    def issuperset(self, other):
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported method for'{type(self)}' and {type(other)}")
        return self._edges.issuperset(other._edges)

    def clear(self):
        self._edges.clear()

    def copy(self):
        result = EdgeSet()
        result._edges = self._edges.copy()
        return result
