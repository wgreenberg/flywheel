import unittest

from lib.graph import Vertex, Edge, Graph

# All examples here from http://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm

class TestExample1(unittest.TestCase):
    a, b, c, d = [Vertex(l) for l in 'ABCD']
    edges = [
        Edge(a, b, 1),
        Edge(a, c, 1),
        Edge(c, a, 1),
        Edge(b, c, 1),
        Edge(d, c, 1),
    ]
    g = Graph([a,b,c,d], edges)

    def test_graph_connection_cache(self):
        self.assertEqual(self.g.inV[self.a], set([(self.c, 1)]))
        self.assertEqual(self.g.inV[self.b], set([(self.a, 1)]))
        self.assertEqual(self.g.inV[self.c], set([(self.a, 1), (self.b, 1), (self.d, 1)]))
        self.assertEqual(self.g.inV[self.d], set())

        self.assertEqual(self.g.outV[self.a], set([(self.b, 1), (self.c, 1)]))
        self.assertEqual(self.g.outV[self.b], set([(self.c, 1)]))
        self.assertEqual(self.g.outV[self.c], set([(self.a, 1)]))
        self.assertEqual(self.g.outV[self.d], set([(self.c, 1)]))

    def test_pagerank(self):
        pr_result = self.g.pagerank()
        self.assertAlmostEqual(pr_result[self.a], 1.49, places=2)
        self.assertAlmostEqual(pr_result[self.b], 0.78, places=2)
        self.assertAlmostEqual(pr_result[self.c], 1.58, places=2)
        self.assertAlmostEqual(pr_result[self.d], 0.15, places=2)

class TestExample2(unittest.TestCase):
    home = Vertex('Home')
    about = Vertex('About')
    product = Vertex('Product')
    links = Vertex('Links')
    a = Vertex('External Site A')
    b = Vertex('External Site B')
    c = Vertex('External Site C')
    d = Vertex('External Site D')
    edges = [
        Edge(home, about, 1), Edge(about, home, 1),
        Edge(home, product, 1), Edge(product, home, 1),
        Edge(home, links, 1), Edge(links, home, 1),
        Edge(links, a, 1),
        Edge(links, b, 1),
        Edge(links, c, 1),
        Edge(links, d, 1),
    ]
    g = Graph([home, about, product, links, a, b, c, d], edges)

    def test_pagerank(self):
        pr_result = self.g.pagerank()
        self.assertAlmostEqual(pr_result[self.home], 0.92, places=2)
        self.assertAlmostEqual(pr_result[self.about], 0.41, places=2)
        self.assertAlmostEqual(pr_result[self.product], 0.41, places=2)
        self.assertAlmostEqual(pr_result[self.links], 0.41, places=2)
        self.assertAlmostEqual(pr_result[self.a], 0.22, places=2)
        self.assertAlmostEqual(pr_result[self.b], 0.22, places=2)
        self.assertAlmostEqual(pr_result[self.c], 0.22, places=2)
        self.assertAlmostEqual(pr_result[self.d], 0.22, places=2)
