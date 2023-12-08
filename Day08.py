import math


# Get data from .txt file
def get_input() -> tuple[list, dict]:
    with open('input/Day08.txt', 'r') as file:
        # Split lines, and write each line to list
        data = file.read().splitlines()
        # Get instructions and convert to indices
        dict_instructions = {'L': 0, 'R': 1}
        instructions = [dict_instructions[char] for char in data[0]]
        # Get maps
        mapper = {}
        for line in data[2:]:
            # Split strings and create mapper dictionary
            start, end = line.split(' = ')
            mapper[start] = end[1:-1].split(', ')
    return instructions, mapper


# Solves part 1
def part_one(instructions: list, mapper: dict) -> int:
    # Starting position
    current_index = 'AAA'
    # Index of the instructions
    instructions_index = 0
    # Initialize count of steps
    count = 0
    # While we haven't reached our target position, keep stepping
    while current_index != 'ZZZ':
        current_index = mapper[current_index][instructions[instructions_index]]
        # Update instructions index (modulo to wrap around when we reached the end) and count
        instructions_index = (instructions_index + 1) % len(instructions)
        count += 1
    return count


# Solves part 2
# This part as initially just checking if all positions end up in a position that ends in 'Z' at any given step.
# Unfortunately, this doesn't work because there are too many steps. Thus, we need to look for cycles where we see
# repetition in steps. This way we can evaluate every starting position separately and in the end calculate the LCM
def part_two(instructions: list, mapper: dict) -> int:
    # Get all starting positions that end in an A
    starting_positions = [key for key in mapper if key.endswith('A')]
    # Initialize cycles
    cycles = []
    # Loop through all possible starting positions
    for new_pos in starting_positions:
        prev_pos = ''
        new_index = 0
        prev_index = 0
        visited = set()
        count = 0
        # Keep stepping until we see that the previous position was a valid end position and the current position with
        # the same instruction (in the entire string of instructions, same string position) has been seen before --> we
        # found a cycle. Note that here we have complete cycles, meaning that the first position after the starting
        # position is already part of the cycle would that not be the case, we need to find the path length to the cycle
        # and our LCM calculations would need to consider that.
        while not (prev_pos.endswith('Z') and (new_pos, prev_index) in visited):
            # Save prev pos to check later if it ended with a Z
            prev_pos = new_pos
            # Save previous index, because it's actually the index of the new position, but we update it below to a
            # "future_index"
            prev_index = new_index
            # Get new position
            new_pos = mapper[new_pos][instructions[new_index]]
            # Add this position to the visited positions
            visited.add((new_pos, new_index))
            # Update instructions index (modulo to wrap around when we reached the end) and count
            new_index = (new_index + 1) % len(instructions)
            count += 1
        # Add to cycle
        cycles.append(count - 1)
    # Calculate LCM
    return math.lcm(*cycles)


def main():
    instructions, mapper = get_input()
    print('This many steps are required to reach ZZZ:', part_one(instructions, mapper))
    print("It take this many steps before you're only on nodes that end with Z:", part_two(instructions, mapper))


if __name__ == '__main__':
    main()
