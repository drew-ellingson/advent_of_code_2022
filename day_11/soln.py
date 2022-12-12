import math
from copy import deepcopy


class Monkey:
    def __init__(self, monkey_str):
        parsed = self._parse_monkey(monkey_str)

        self.label = parsed[0]
        self.items = parsed[1]
        self.operation = parsed[2]
        self.test_divisor = parsed[3]
        self.test = parsed[4]
        self.true_target = parsed[5]
        self.false_target = parsed[6]

        self.items_inspected = 0

    def __repr__(self):
        return f"""
label: {self.label}
current_items: {self.items}
operation: {self.operation}
test: {self.test}
true_target: {self.true_target}
false_target: {self.false_target}\n"""

    def _parse_monkey(self, monkey):
        lines = [line.strip() for line in monkey.split("\n")]

        # remove trailing semicolon to get pure number label
        label = int(lines[0][:-1].split()[-1])

        items = lines[1][lines[1].index(":") + 1 :]
        items = [int(x) for x in items.split(",")]

        # take function rule directly from text
        operation = lambda old: eval(lines[2][lines[2].index("=") + 1 :])

        # all test functions are divisbility
        test_divisor = int(lines[3].split()[-1])
        test = lambda x: x % test_divisor == 0

        true_target = int(lines[4].split()[-1])
        false_target = int(lines[5].split()[-1])

        return label, items, operation, test_divisor, test, true_target, false_target


class Game:
    def __init__(self, monkeys, rounds):
        self.monkeys = monkeys
        self.rounds = rounds
        self.modulus = math.prod(m.test_divisor for m in monkeys)

    def monkey_turn(self, m, p2=False):
        for item in m.items:
            item = (m.operation(item) if p2 else m.operation(item) // 3) % self.modulus
            tgt_label = m.true_target if m.test(item) else m.false_target
            self.monkeys[tgt_label].items.append(item)
            m.items_inspected += 1

        m.items.clear()

    def round(self, p2=False):
        for m in self.monkeys:
            self.monkey_turn(m, p2=p2)

    def play_full_game(self, p2=False):
        for r in range(self.rounds):
            self.round(p2=p2)

    def monkey_business_score(self):
        top_monkeys = sorted(
            self.monkeys, key=lambda m: m.items_inspected, reverse=True
        )[:2]
        return math.prod([m.items_inspected for m in top_monkeys])


with open("input.txt") as my_file:
    monkeys = [Monkey(m) for m in my_file.read().split("\n\n")]
    rounds = 20

    p2_monkeys = deepcopy(monkeys)
    p2_rounds = 10000

game = Game(monkeys, rounds)
game.play_full_game()

print(f"P1 Solution is: {game.monkey_business_score()}")

game = Game(p2_monkeys, p2_rounds)
game.play_full_game(p2=True)

print(f"P2 Solution is: {game.monkey_business_score()}")
