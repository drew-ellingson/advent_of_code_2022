from copy import copy


def parse_inst(inst_line):
    direc, mag = inst_line.strip().split()
    mag = int(mag)
    return (direc, mag)


def _mult(tup, scal):
    return tuple(scal * x for x in tup)


def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))


def _diff(tup1, tup2):
    return _add(tup1, _mult(tup2, -1))


def get_new_follow_pos(lead_pos, follow_pos):
    diff = _diff(lead_pos[-1], follow_pos[-1])
    move = (
        (int((a > 0) - (a < 0)) for a in diff)  # sign one liner
        if any(abs(a) >= 2 for a in diff)
        else (0, 0)
    )
    return _add(follow_pos[-1], move)


def do_instr(instr, knots_pos):
    for _ in range(instr[1]):
        knots_pos[0].append(_add(knots_pos[0][-1], dirs[instr[0]]))  # move head
        for i in range(1, len(knots_pos)):
            knots_pos[i].append(get_new_follow_pos(knots_pos[i - 1], knots_pos[i]))


def all_instr(instrs, knots_pos):
    for i in instrs:
        do_instr(i, knots_pos)


with open("input.txt") as my_file:
    instrs = [parse_inst(line) for line in my_file.readlines()]
    p2_instrs = copy(instrs)

dirs = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}

knots_pos = [[(0, 0)] for _ in range(2)]
all_instr(instrs, knots_pos)
print(f"P1 Answer is: {len(set(knots_pos[-1]))}")

knots_pos = [[(0, 0)] for _ in range(10)]
all_instr(p2_instrs, knots_pos)
print(f"P2 Answer is: {len(set(knots_pos[-1]))}")
