import re
from collections import namedtuple

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))


def _mult(tup1, scal):
    return tuple(scal * a for a in tup1)

def _diff(tup1, tup2):
    return _add(tup1, _mult(tup2, -1))

def _mag(tup1): # manhattan
    return abs(tup1[0]) + abs(tup1[1])

excludedCoord = namedtuple('excludedCoord', ['length', 'min_x', 'max_x'])

class Sensor:
    def __init__(self, sensor, closest_beacon):
        self.sensor = sensor 
        self.closest_beacon = closest_beacon
        self.exc_radius = _mag(_diff(sensor, closest_beacon))

    def get_exclusion_bounds(self, row):
        x_center = self.sensor[0]
        y_diff = abs(self.sensor[1] - row)
        
        # both ends inclusive
        return (x_center - self.exc_radius + y_diff, x_center + self.exc_radius - y_diff)

class Grid:
    def __init__(self, sensors):
        self.sensors = sensors # object

    def count_excluded_pos(self, row):
        min_x, max_x = None, None 

        for s in self.sensors:
            curr_min_x, curr_max_x = s.get_exclusion_bounds(row)

            try:
                min_x = min(min_x, curr_min_x)
                max_x = max(max_x, curr_max_x)
            except TypeError:
                min_x = curr_min_x
                max_x = curr_max_x
    
        row_objects = [o for o in set(beacons + sensors) if o[1] == row and min_x <= o[0] <= max_x]
        
        return excludedCoord(max_x - min_x + 1 - len(row_objects), min_x, max_x)

    def find_missing_beacon(self, max_x, max_y):
        for i in range(max_y + 1):
            excluded_coords = self.count_excluded_pos(i)
            print(i, excluded_coords)
            if excluded_coords[1] > 0 or excluded_coords[2] < max_x:
                print(i, excluded_coords)

    def score(self, x, y):
        return 4000000 * x + y

def parse_object(obj):
    # remove non-numeric characters and get coord as tuple of ints
    coords = re.sub(r'[^0-9,-]', '', obj)
    return tuple(int(a) for a in coords.split(','))

with open('input2.txt') as my_file:
    lines = my_file.readlines()
    sensors = [parse_object(x.split(':')[0]) for x in lines]
    beacons = [parse_object(x.split(':')[1]) for x in lines]

sens_objs = [Sensor(sensors[i], beacons[i]) for i in range(len(sensors))]

grid = Grid(sens_objs)
row = 10
bound = 20

print(f'P1 Soln is: {grid.count_excluded_pos(row).length}')

print(f'P2 Soln is: {grid.find_missing_beacon(bound, bound)}')