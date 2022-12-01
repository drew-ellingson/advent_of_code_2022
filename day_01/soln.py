with open("input.txt") as my_file:
    elves = [
        [int(cal.strip()) for cal in elf.split("\n")]
        for elf in my_file.read().split("\n\n")
    ]

print(f"P1 Soln is: {max(sum(elf) for elf in elves)}")

elves.sort(key=lambda x: sum(x), reverse=True)

print(f"P2 Soln is: {sum(sum(elf) for elf in elves[:3])}")
