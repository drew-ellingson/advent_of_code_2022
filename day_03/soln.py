with open("input.txt") as my_file:
    sacks = [line.strip() for line in my_file.readlines()]
    sacks = [[sack[: int(len(sack) / 2)], sack[int(len(sack) / 2) :]] for sack in sacks]


def score_letter(letter):
    if letter.islower():
        return ord(letter) - ord("a") + 1
    else:
        return ord(letter) - ord("A") + 26 + 1


def score_sack(sack):
    common = list(set([x for x in sack[0] if x in sack[1]]))

    if len(common) != 1:
        raise (
            ValueError(
                f"Sack: {sack} has letters in common {common}, which has len > 1"
            )
        )

    return score_letter(common[0])


print(f"P1 Soln is: {sum(score_sack(sack) for sack in sacks)}")


def list_groups(li, n):
    for i in range(0, len(li), n):
        yield li[i : i + n]


with open("input.txt") as my_file:
    groups = [line.strip() for line in my_file.readlines()]
    groups = list(list_groups(groups, 3))


def score_sack_p2(sack_triple):
    common = list(
        set([x for x in sack_triple[0] if x in sack_triple[1] and x in sack_triple[2]])
    )

    if len(common) != 1:
        raise (
            ValueError(
                f"Sack Triple: {sack_triple} has letters in common {common}, which has len > 1"
            )
        )

    return score_letter(common[0])


print(f"P2 Soln is: {sum(score_sack_p2(sack_triple) for sack_triple in groups)}")
