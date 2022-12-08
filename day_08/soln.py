class TreeGrid:
    def __init__(self, raw_grid):
        self.grid = raw_grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def is_visible(self, x, y):
        if x == 0 or x == self.width or y == 0 or y == self.height:
            return True

        curr = self.grid[y][x]

        left_vis = all(self.grid[j][x] < curr for j in range(y))
        right_vis = all(self.grid[j][x] < curr for j in range(y + 1, self.height))
        top_vis = all(self.grid[y][i] < curr for i in range(x))
        bottom_vis = all(self.grid[y][i] < curr for i in range(x + 1, self.width))

        return any([left_vis, right_vis, top_vis, bottom_vis])

    def count_visible_trees(self):
        return sum(
            [
                self.is_visible(x, y)
                for y in range(self.height)
                for x in range(self.width)
            ]
        )

    def scenic_score(self, x, y):
        curr = self.grid[y][x]

        # defaults account for case where all trees in a direction are shorter than curr        
        left_score = x - max([i for i in range(x) if self.grid[y][i] >= curr], default=0)
        right_score = min([i for i in range(x + 1, self.width) if self.grid[y][i] >= curr], default=self.width - 1 ) - x
        top_score = y - max([j for j in range(y) if self.grid[j][x] >= curr], default=0)
        bottom_score = min([j for j in range(y + 1, self.height) if self.grid[j][x] >= curr], default=self.height - 1) - y

        return left_score * right_score * top_score * bottom_score

    def most_scenic_tree(self):
        return max(
            self.scenic_score(x, y)
            for y in range(self.height)
            for x in range(self.width)
        )


with open("input.txt") as my_file:
    grid = [[int(val) for val in row.strip()] for row in my_file.readlines()]

grid = TreeGrid(grid)

print(f"P1 Soln is: {grid.count_visible_trees()}")
print(f"P2 Soln is: {grid.most_scenic_tree()}")
