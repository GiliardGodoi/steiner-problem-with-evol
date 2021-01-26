
class GEdge:
    pass

class DEdge(GEdge):
    pass

class UEdge(GEdge):
    pass

class EdgeSet:

    @classmethod
    def _format_edge(self, item):
        if len(item) != 2:
            raise ValueError(f"Edge must have 2 ending points. This has {len(item)} elements: {item}")
        return (min(item), max(item))

    def __init__(self,items):

        assert len(items) > 0, "Could not create a empty EdgeSet"

        self._edges = set()

        if isinstance(items, (list, tuple, set)):
            for item in items:
                self._edges.add(self._format_edge(item))

    def __str__(self):
        pass

    def __repr__(self):
        pass

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
        return self._edges - other._edges

    def __and__(self, other):
        '''& operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for &: '{type(self)}' and {type(other)}")
        return self._edges & other._edges

    def __xor__(self, other):
        '''^ operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for ^: '{type(self)}' and {type(other)}")
        return self._edges ^ other._edges

    def __or__(self, other):
        ''' | operator'''
        if not isinstance(other, EdgeSet):
            raise TypeError(f"unsupported operand type(s) for -: '{type(self)}' and {type(other)}")
        return self._edges | other._edges

    def __eq__(self, other):
        '''== operator '''
        pass

    def __lt__(self, other):
        '''< operator '''
        pass

    def __le__(self, other):
        '''<= operator '''
        pass

    def __gt__(self, other):
        '''> operator '''
        pass

    def __ge__(self, other):
        '''>= operator '''
        pass

    @property
    def vertices(self):
        pass

    def add(self, edge):
        self._edges.add(self._format_edge(edge))

    def discard(self, edge):
        edge = self._format_edge(edge)
        self._edges.discard(edge)

    def remove(self, edge):
        edge = self._format_edge(edge)
        self._edges.remove(edge)

    def issubset(self, other):
        pass

    def issuperset(self, other):
        pass

    def clear(self):
        self._edges.clear()

    def copy(self):
        return self._edges.copy()
