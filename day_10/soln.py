from collections import namedtuple


def parse_instr(instr_line):
    if instr_line.startswith("addx"):
        op, val = instr_line.split()
        val = int(val)
    else:
        op, val = instr_line, 0
    return op, val


with open("input.txt") as my_file:
    instrs = [parse_instr(line.strip()) for line in my_file.readlines()]

# renamed x to val so i dind't confuse myself with position
State = namedtuple("State", ["cycle", "val"])
states = [State(0, 1)]


def do_instr(instr, states):
    last = states[-1]
    if instr[0] == "noop":
        states.append(State(last.cycle + 1, last.val))
    else:
        states.append(State(last.cycle + 2, last.val + instr[1]))


def do_all_instr(instrs):
    for i in instrs:
        do_instr(i, states)


def score(states):
    max_cycle = states[-1].cycle

    # this isnt good but i cant think today
    score_indices = [20 + 40 * i for i in range(6)]
    score_states = [
        max([s for s in states if s.cycle < si], key=lambda a: a.cycle)
        for si in score_indices
    ]

    return sum(map(lambda a: a[0] * a[1].val, zip(score_indices, score_states)))


def draw(states):
    # indexing a bit weird to get it to line up in the image
    all_cycles = [
        max(
            (s for s in states if s.cycle < i), key=lambda a: a.cycle, default=states[0]
        )
        for i in range(1, 241)
    ]

    for i in range(6):
        row = [
            "#" if abs(all_cycles[j].val - (j % 40)) <= 1 else "."
            for j in range(40 * i, 40 * (i + 1))
        ]
        print("".join(row))


do_all_instr(instrs)
print(f"P1 Soln is: {score(states)}")

print("P2 Soln is:")
draw(states)
