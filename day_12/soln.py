
from collections import namedtuple

class GraphMatrix:
    def __init__(self, raw_matrix):
        parsed = self.parse_raw_matrix(raw_matrix)

        self.h = parsed[0]
        self.w = parsed[1]
        self.start = parsed[2]
        self.end = parsed[3]
        self.vals = parsed[4]

        self.edges = self.get_edges()

    def parse_raw_matrix(self, raw_matrix):
        h = len(raw_matrix.split('\n'))
        w = len(raw_matrix.split('\n')[0])

        # flatten    
        vals = [val for row in raw_matrix.replace('\n','') for val in row ]
        
        start = vals.index('S')
        end = vals.index('E')

        vals[start], vals[end] = 'a', 'z'
        vals = [ord(val) - 97 for val in vals]

        return h, w, start, end, vals
    
    def get_edges(self):
        edges = []
        for i in range(len(self.vals)):
            # right, left, down, up
            cands = [i + 1, i - 1, i + self.w, i - self.w]
            
            # check up and down adjs are actually within the grid
            within_grid = [tgt for tgt in cands if tgt >= 0 and tgt <= len(self.vals) - 1]

            # left edge not adj to right edge of previous row
            # right edge not adj to left edge of following row
            borders_dont_wrap = [tgt for tgt in within_grid if not ((i % self.w == 0 and tgt == i - 1) or (i % self.w == self.w - 1 and tgt == i + 1))]

            # check height is appropriate to move from src to tgt
            adjs = [tgt for tgt in borders_dont_wrap if self.vals[tgt] <= self.vals[i] + 1]

            edges.extend([(i, tgt) for tgt in adjs])
        return edges

def path_costs(graph):
    edge_cost = namedtuple('edge_cost', ['src', 'tgt', 'cost'])
    visited = [False if i != 0 else True for i in range(len(graph.vals))]
    costs = [None if i != 0 else 0 for i in range(len(graph.vals))]

    queue = []
    queue.extend(edge_cost(src, tgt, 1) for (src, tgt) in graph.edges if src == graph.start)

    while not costs[graph.end]:
        curr = queue.pop(0)
        if not visited[curr.tgt]:
            visited[curr.tgt] = True
            costs[curr.tgt] = curr.cost
            next_nodes = [edge_cost(src, tgt, curr.cost + 1) for (src, tgt) in graph.edges if src == curr.tgt]
            queue.extend(next_nodes)

    return costs[graph.end]

with open('input.txt') as my_file: 
    raw_matrix = my_file.read()

graph = GraphMatrix(raw_matrix)

print(f'P1 Soln is: {path_costs(graph)}')

