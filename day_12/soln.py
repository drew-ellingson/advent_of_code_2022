from collections import namedtuple


class GraphMatrix:
    def __init__(self, h, w, vals):

        self.h = h
        self.w = w
        self.vals = vals

        self.edges = self.get_edges()

    def get_edges(self):
        edges = []
        for i in range(len(self.vals)):
            # right, left, down, up
            cands = [i + 1, i - 1, i + self.w, i - self.w]

            # check up and down adjs are actually within the grid
            within_grid = [
                tgt for tgt in cands if tgt >= 0 and tgt <= len(self.vals) - 1
            ]

            # left edge not adj to right edge of previous row
            # right edge not adj to left edge of following row
            borders_dont_wrap = [
                tgt
                for tgt in within_grid
                if not (
                    (i % self.w == 0 and tgt == i - 1)
                    or (i % self.w == self.w - 1 and tgt == i + 1)
                )
            ]

            # check height is appropriate to move from src to tgt
            adjs = [
                tgt for tgt in borders_dont_wrap if self.vals[tgt] <= self.vals[i] + 1
            ]

            edges.extend([(i, tgt) for tgt in adjs])
        return edges


def path_costs(graph, start, end):
    edge_cost = namedtuple("edge_cost", ["src", "tgt", "cost"])

    visited = [False if i != start else True for i in range(len(graph.vals))]
    costs = [None if i != start else 0 for i in range(len(graph.vals))]

    queue = []
    queue.extend(edge_cost(src, tgt, 1) for (src, tgt) in graph.edges if src == start)

    while not costs[end]:
        try:
            curr = queue.pop(0)
        except:
            return len(graph.vals)  # safe upper bound

        if not visited[curr.tgt]:
            visited[curr.tgt] = True
            costs[curr.tgt] = curr.cost
            next_nodes = [
                edge_cost(src, tgt, curr.cost + 1)
                for (src, tgt) in graph.edges
                if src == curr.tgt
            ]

            queue.extend(next_nodes)

    return costs[end]


with open("input.txt") as my_file:
    raw_matrix = my_file.read()

    # gonna write over these with heights, so want to keep a record
    start = raw_matrix.replace("\n", "").index("S")
    end = raw_matrix.replace("\n", "").index("E")


def parse_raw_matrix(raw_matrix):
    h = len(raw_matrix.split("\n"))
    w = len(raw_matrix.split("\n")[0])

    # flatten
    vals = [val for row in raw_matrix.replace("\n", "") for val in row]
    vals[vals.index("S")], vals[vals.index("E")] = "a", "z"
    vals = [ord(val) - 97 for val in vals]

    return h, w, vals


graph = GraphMatrix(*parse_raw_matrix(raw_matrix))
p1_cost = path_costs(graph, start, end)
print(f"P1 Soln is: {p1_cost}")

starts = [i for i in range(len(graph.vals)) if graph.vals[i] == 0]
print(f"P2 Soln is: {min(path_costs(graph, s, end) for s in starts)}")
