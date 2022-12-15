import math


def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))


def _mult(tup1, scal):
    # this will always be int for our context. bad assumption generally
    return tuple(int(scal * a) for a in tup1)


def _diff(tup1, tup2):
    return _add(tup1, _mult(tup2, -1))


def _mag(tup1):
    # this will always be int for our context. bad assumption generally
    return int(math.sqrt(tup1[0] ** 2 + tup1[1] ** 2))


class Grid:
    def __init__(self, rock_corners):
        self.rocks = self.get_all_rock_coords(rock_corners)

        # adding some padding - shouldn't matter
        self.min_x = min(a[0] for a in self.rocks) - 2
        self.max_x = max(a[0] for a in self.rocks) + 2
        self.min_y = 0
        self.max_y = max(a[1] for a in self.rocks) + 2

        print(self.min_x, self.max_x, self.min_y, self.max_y)

        # tuple-indexed grid. might be slow as hell
        self.grid = {
            (i, j): "#" if (i, j) in self.rocks else "."
            for i in range(self.min_x, self.max_x)
            for j in range(self.min_y, self.max_y)
        }

    def __repr__(self):
        msg = ""
        for j in range(self.min_y, self.max_y):
            msg = f"{msg}\n{''.join(self.grid[(i, j)] for i in range(self.min_x, self.max_x))}"
        return msg

    def _next_pos(self, coord):
        x, y = coord
        if self.grid[(x, y + 1)] == ".":
            return (x, y + 1)
        elif self.grid[(x - 1, y + 1)] == ".":
            return (x - 1, y + 1)
        elif self.grid[(x + 1, y + 1)] == ".":
            return (x + 1, y + 1)
        else:
            return (x, y)

    def add_one_sand(self):
        sand_pos = (500, 0)
        while sand_pos != self._next_pos(sand_pos):
            sand_pos = self._next_pos(sand_pos)
        self.grid[sand_pos] = "o"

    def get_capacity(self):
        cap = 0
        try:
            while True:
                if self.grid[(500, 0)] == "o":  # sand at rest at source
                    return cap
                self.add_one_sand()
                cap += 1
        except KeyError:  # sand falling into abyss
            return cap

    def get_all_rock_coords(self, rock_corners):
        rocks = []
        for rock_set in rock_corners:
            for i in range(len(rock_set) - 1):
                diff = _diff(rock_set[i + 1], rock_set[i])

                # unit
                u_diff = _mult(diff, 1 / _mag(diff))

                rocks.extend(
                    [_add(rock_set[i], _mult(u_diff, j)) for j in range(_mag(diff) + 1)]
                )
        return rocks


def parse(rock_line):
    return [
        tuple(int(x) for x in coord.split(",")) for coord in rock_line.split(" -> ")
    ]


with open("input.txt") as my_file:
    rocks = [parse(line) for line in my_file.readlines()]

grid = Grid(rocks)
print(f"P1 Soln is: {grid.get_capacity()}")

# sand cannot rest farther to left or right than max_y. Adding this wall simulates an infinite grid
p2_rocks = rocks + [
    [(500 - grid.max_y - 5, grid.max_y), (500 + grid.max_y + 5, grid.max_y)]
]
p2_grid = Grid(p2_rocks)
print(f"P2 Soln is: {p2_grid.get_capacity()}")
