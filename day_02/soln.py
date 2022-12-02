with open("input.txt") as my_file:
    rounds = [line.strip().split(" ") for line in my_file.readlines()]

wins = {"A": "Y", "B": "Z", "C": "X"}
losses = {"A": "Z", "B": "X", "C": "Y"}
draws = {"A": "X", "B": "Y", "C": "Z"}


def score(round, p2=False):

    if p2:
        round[1] = (
            wins[round[0]]
            if round[1] == "Z"
            else draws[round[0]]
            if round[1] == "Y"
            else losses[round[0]]
        )

    letter_score = ord(round[1]) - ord("X") + 1
    round_score = 3 * (
        1 + (wins.get(round[0]) == round[1]) - (losses.get(round[0]) == round[1])
    )
    return letter_score + round_score


print(f"P1 Soln is: {sum(score(round) for round in rounds)}")
print(f"P2 Soln is: {sum(score(round, p2=True) for round in rounds)}")
