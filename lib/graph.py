from collections import namedtuple, defaultdict

Vertex = namedtuple('Vertex', ['data'])
Edge = namedtuple('Edge', ['src', 'dst', 'weight'])

class Graph():
    def __init__(self, V, E):
        self.V = V
        self.E = E

        # build a cache of in/out sets for the vertices
        self.inV, self.outV = self._build_cache()

        # start each vertex with arbitrary score
        self._pr_scores = defaultdict(lambda: 1)

        # PageRank params
        self._pr_d = 0.85
        self._pr_num_iter = 20

    def _build_cache(self):
        inV = defaultdict(set)
        outV = defaultdict(set)
        for e in self.E:
            inV[e.dst].add((e.src, e.weight))
            outV[e.src].add((e.dst, e.weight))
        return inV, outV

    def pagerank(self):
        for i in range(self._pr_num_iter):
            for v in self.V:
                self._pr_scores[v] = self._recalculate(v)
        return self._pr_scores

    def _recalculate(self, v_i):
        new_score = 0
        for v_j, v_ji_weight in self.inV[v_i]:
            v_j_score = self._pr_scores[v_j]
            v_jk_weight_sum = sum([w_jk for (v_k, w_jk) in self.outV[v_j]])
            new_score += (v_ji_weight / v_jk_weight_sum) * v_j_score
        new_score *= self._pr_d
        new_score += 1 - self._pr_d
        return new_score
