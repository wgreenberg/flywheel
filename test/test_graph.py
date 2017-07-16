import unittest

from lib.graph import Vertex, Edge, Graph

# All examples here from http://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm

class TestExample1(unittest.TestCase):
    a, b, c, d = [Vertex(l) for l in 'ABCD']
    edges = [
        Edge(a, b, 0),
        Edge(a, c, 0),
        Edge(c, a, 0),
        Edge(b, c, 0),
        Edge(d, c, 0),
    ]
    g = Graph([a,b,c,d], edges)

    def test_graph_connection_cache(self):
        self.assertEqual(self.g.inV[self.a], set([self.c]))
        self.assertEqual(self.g.inV[self.b], set([self.a]))
        self.assertEqual(self.g.inV[self.c], set([self.a, self.b, self.d]))
        self.assertEqual(self.g.inV[self.d], set())

        self.assertEqual(self.g.outV[self.a], set([self.b, self.c]))
        self.assertEqual(self.g.outV[self.b], set([self.c]))
        self.assertEqual(self.g.outV[self.c], set([self.a]))
        self.assertEqual(self.g.outV[self.d], set([self.c]))

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
        Edge(home, about, 0), Edge(about, home, 0),
        Edge(home, product, 0), Edge(product, home, 0),
        Edge(home, links, 0), Edge(links, home, 0),
        Edge(links, a, 0),
        Edge(links, b, 0),
        Edge(links, c, 0),
        Edge(links, d, 0),
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
