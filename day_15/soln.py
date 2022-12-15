import re


def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))


def _mult(tup1, scal):
    return tuple(scal * a for a in tup1)


def _diff(tup1, tup2):
    return _add(tup1, _mult(tup2, -1))


def _mag(tup1):  # manhattan
    return abs(tup1[0]) + abs(tup1[1])


def _min_cover(intervals):
    """takes a list of overlapping closed intervals (as tuples) and
    provides a minimum disjoint set of equivalent intervals
    """
    min_cover = []
    intervals = [x for x in intervals if x[1] > x[0]]  # omit bogus

    for begin, end in sorted(intervals):
        if min_cover and min_cover[-1][1] >= begin:
            min_cover[-1] = (min_cover[-1][0], max(min_cover[-1][1], end))
        else:
            min_cover.append((begin, end))
    return min_cover


class Sensor:
    def __init__(self, sensor, closest_beacon):
        self.sensor = sensor
        self.closest_beacon = closest_beacon
        self.exc_radius = _mag(_diff(sensor, closest_beacon))

    def get_exclusion_bounds(self, row):
        x_center = self.sensor[0]
        y_diff = abs(self.sensor[1] - row)

        # both ends inclusive
        return (
            x_center - self.exc_radius + y_diff,
            x_center + self.exc_radius - y_diff,
        )


class Grid:
    def __init__(self, sensors):
        self.sensors = sensors  # object

    def get_excluded_pos(self, row):
        bounds = [s.get_exclusion_bounds(row) for s in self.sensors]
        obj_bounds = [(o[0], o[0]) for o in set(beacons + sensors) if o[1] == row]
        return _min_cover(bounds + obj_bounds)

    def count_excluded_pos(self, row):
        intervals = self.get_excluded_pos(row)
        return sum(x[1] - x[0] for x in intervals)

    def find_missing_beacon(self, max_x, max_y):
        for i in range(1, max_y + 1):
            bounds = self.get_excluded_pos(i)

            # there exists an interval that covers our beacon range
            if any(b[0] <= 0 and b[1] >= max_x for b in bounds):
                continue

            return (bounds[0][1] + 1, i)  # pos of missing beacon

    def score(self, x, y):
        return 4000000 * x + y


def parse_object(obj):
    # remove non-numeric characters and get coord as tuple of ints
    coords = re.sub(r"[^0-9,-]", "", obj)
    return tuple(int(a) for a in coords.split(","))


# input2.txt params
filename = "input2.txt"
row = 10
bound = 20

# input.txt params, comment out for testing
filename = "input.txt"
row = 2000000
bound = 4000000

with open(filename) as my_file:
    lines = my_file.readlines()
    sensors = [parse_object(x.split(":")[0]) for x in lines]
    beacons = [parse_object(x.split(":")[1]) for x in lines]

sens_objs = [Sensor(sensors[i], beacons[i]) for i in range(len(sensors))]
grid = Grid(sens_objs)
print(f"P1 Soln is: {grid.count_excluded_pos(row)}")

missing_beacon = grid.find_missing_beacon(bound, bound)
print(f"P2 Soln is: {grid.score(*missing_beacon)}")
