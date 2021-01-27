from random import randint
from itertools import count
import unittest
from typing import Generator, Iterator

from ga4stpg.edgeset import EdgeSet, UEdge


class TestEdgeSet(unittest.TestCase):

    def test_init_empty(self):
        edset = EdgeSet()
        self.assertFalse(len(edset))

    def test_init_with_list_of_tuples(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = list((next(A), next(B)) for _ in range(200))

        self.assertIsInstance(items, list)
        self.assertTrue(all(isinstance(item, tuple) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)

    def test_init_with_list_of_edges(self):
        raise NotImplementedError()

    def test_init_with_tuple_of_tuples(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = tuple((next(A), next(B)) for _ in range(200))

        self.assertIsInstance(items, tuple)
        self.assertTrue(all(isinstance(item, tuple) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)

    def test_init_with_tuple_of_edges(self):
        raise NotImplementedError()

    def test_init_with_set_of_tuples(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = {(next(A), next(B)) for _ in range(200)}

        self.assertIsInstance(items, set)
        self.assertTrue(all(isinstance(item, tuple) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)


    def test_init_with_set_of_edges(self):
        raise NotImplementedError()

    def test_init_with_edgeset(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        other = EdgeSet(result)

        self.assertFalse(other is result)
        self.assertFalse(other._edges is result._edges)
        self.assertEqual(result, other)
        self.assertEqual(other._edges, result._edges)
        self.assertEqual(len(result), len(other))

    def test_contains(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]
        result = EdgeSet(items)

        self.assertTrue(hasattr(result, "__contains__"))
        self.assertTrue(UEdge(8, 9) in result)
        self.assertTrue(UEdge(9, 8) in result)

        self.assertFalse(UEdge(8, 7) in result)
        self.assertFalse(UEdge(7, 8) in result)

    def test_if_is_iterable(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        self.assertTrue(hasattr(result, '__iter__'))

        self.assertIsInstance(iter(result), Iterator)

        total = 0

        for _ in result:
            total += 1

        self. assertEqual(len(result), total)

        total_again = 0
        for _ in result:
            total_again += 1

        self.assertEqual(total, total_again)

    def test_len_property(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        with self.subTest("How many edges?"):
            self.assertEqual(len(result), 200)

        with self.subTest("How many edges? len(items)"):
            self.assertEqual(len(result), len(items))

    def test_sub_operand(self):
        raise NotImplementedError()

    def test_and_operand(self):
        raise NotImplementedError()

    def test_xor_operand(self):
        raise NotImplementedError()

    def test_or_operand(self):
        raise NotImplementedError()

    def test_eq_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        obj_1 = EdgeSet((next(A), next(B)) for _ in range(200))

        C = count(398, step=-2)
        D = count(399, step=-2)

        obj_2 = EdgeSet((next(C), next(D)) for _ in range(200))

        self.assertTrue(obj_2 == obj_1)
        self.assertTrue(obj_1 == obj_2)

    def test_not_equal_operand(self):
        raise NotImplementedError()

    def test_less_than_operand(self):
        raise NotImplementedError()

    def test_greater_than_operand(self):
        raise NotImplementedError()

    def test_greater_or_equal_opearand(self):
        raise NotImplementedError()

    def test_less_or_equal_operand(self):
        raise NotImplementedError()

    def test_vertices_property(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [(next(A), next(B)) for _ in range(200)]
        result = EdgeSet(items)

        self.assertTrue(hasattr(result, 'vertices'))
        self.assertIsInstance(result.vertices, Generator)

        C = count(0, step=2)
        D = count(1, step=2)
        aa = set(next(C) for _ in range(200))
        bb = set(next(D) for _ in range(200))

        cc = aa.union(bb)

        nodes = [v for v in result.vertices]

        self.assertEqual(len(nodes), len(cc))

    def test_add_method(self):
        raise NotImplementedError()

    def test_discard_method(self):
        raise NotImplementedError()

    def test_remove_method(self):
        raise NotImplementedError()

    def test_issubset_method(self):
        raise NotImplementedError()

    def test_issuperset_method(self):
        raise NotImplementedError()

    def test_clear_method(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        with self.subTest("Has it elements?"):
            self.assertTrue(result)
            self.assertTrue(len(result))
            self.assertEqual(len(result), 200)

        result.clear()

        with self.subTest("There isn't elements anymore."):
            self.assertFalse(result)
            self.assertFalse(len(result))
            self.assertEqual(len(result), 0)

    def test_copy_method(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        copied = result.copy()

        with self.subTest("test instance returned"):
            self.assertIsInstance(copied, EdgeSet)

        with self.subTest("have they same lenght?"):
            self.assertEqual(len(result), len(copied))

        with self.subTest("are they equal?"):
            self.assertTrue(result == copied)
            self.assertTrue(copied == result)

        with self.subTest("are they the same?"):
            self.assertFalse(copied is result)
            self.assertFalse(result is copied)

        with self.subTest("have they the same edges?"):
            self.assertEqual(result._edges, copied._edges)



if __name__ == '__main__':
    unittest.main()
