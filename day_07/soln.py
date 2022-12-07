CURR_PATH = ""


class FileObject:
    def __init__(self, file_line):
        file_line = file_line.strip()
        self.name = file_line.split()[1]

        if file_line.startswith("dir"):
            self.type = "dir"
            self.size = 0
        else:
            self.type = "file"
            self.size = int(file_line.split()[0])

    def __repr__(self):
        return f"{self.type} {self.name} {self.size}"


class Command:
    def __init__(self, command_line):
        global CURR_PATH
        command = command_line.strip().split("\n")

        if command[0].startswith("cd"):
            self.type = "cd"
            self.input = command[0].split(" ")[1]
            self.output = None

            if self.input != "..":
                CURR_PATH = CURR_PATH + "/" + self.input
            else:
                CURR_PATH = "/".join(CURR_PATH.split("/")[:-1])

        if command[0].startswith("ls"):
            self.type = "ls"
            self.input = None
            self.output = [FileObject(o) for o in command[1:]]

        self.curr_path = CURR_PATH

    def __repr__(self):
        return f"folder: {self.curr_path} \ncommand: {self.type} {self.input} \nresults:{self.output}\n"


with open("input.txt") as my_file:
    raw = my_file.read().replace(
        "/", "home"
    )  # dont want to deal with a dir named the same thing as my path sep
    raw_lines = raw.split("\n")
    commands = [Command(c) for c in raw.split("$")[1:]]  # omit first $

# idea for next bit:
# 1. start at dirs containing only direct files
# 2. memoize those dirs sizes into processed_dirs
# 3. continue until all dir sizes are known

processed_dirs = {}
all_dirs = list(
    set([c.curr_path for c in commands if c.type == "cd" and c.input != ".."])
)

while len(processed_dirs) != len(all_dirs):
    rem_dirs = [x for x in all_dirs if x not in processed_dirs.keys()]
    rem_dir_ls = [c for c in commands if c.type == "ls" and c.curr_path in rem_dirs]

    # restrict to only dirs containing files + dirs with known sizes
    known_rem_dir_ls = [
        c
        for c in rem_dir_ls
        if all(
            [
                c.curr_path + "/" + f.name in processed_dirs
                for f in c.output
                if f.type == "dir"
            ]
        )
    ]

    for c in known_rem_dir_ls:
        file_sizes = sum(f.size for f in c.output if f.type == "file")
        dir_sizes = sum(
            processed_dirs[c.curr_path + "/" + f.name]
            for f in c.output
            if f.type == "dir"
        )
        processed_dirs[c.curr_path] = file_sizes + dir_sizes

print(f"P1 Answer is: {sum(v for v in processed_dirs.values() if v <= 100000)}")

total_space, space_needed = 70000000, 30000000
free_space = total_space - processed_dirs["/home"]
free_up_space = space_needed - free_space

print(f"P2 Answer is: {min(v for v in processed_dirs.values() if v >= free_up_space)}")
