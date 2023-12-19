# Get data from .txt file
def get_input() -> tuple[dict, list]:
    with open('input/Day19.txt', 'r') as file:
        # Divide the blocks
        instructions, ratings = file.read().split('\n\n')
        # Split the instructions
        instructions = instructions.split()
        # Split the ratings
        ratings = ratings.split()

        # Create instructions dictionary
        instructions_dict = {}
        # Go through each instruction
        for instruction in instructions:
            # Get the name of the instruction and its instructions
            name, inst = instruction.split('{')
            # Split the instructions into a list
            inst = inst[:-1].split(',')
            # Get the fallback state
            next_state = inst[-1]
            # Go through each instruction in reverse and get its details
            for i, inst_detail in reversed(list(enumerate(inst[:-1]))):
                # Check if we reach the first instruction (in the original list)
                if i == 0:
                    state = name
                # Otherwise create a new state by adding a number
                else:
                    state = name + str(i)
                # Split condition and next state if true
                cond, state_if_true = inst_detail.split(':')
                # Get which category we have from the first char
                cat = 'xmas'.index(cond[0])
                # Get the threshold of the condition
                threshold = int(cond[2:])
                # Adjust the threshold depending on the condition to always be in the format
                # instruction = (cat, threshold, lesser, greater)
                if cond[1] == '<':
                    instruction = (cat, threshold, state_if_true, next_state)
                # If we have the '>' condition, we need to add + 1 to the threshold for our conversion
                else:
                    instruction = (cat, threshold + 1, next_state, state_if_true)
                # Add the new instruction to our dictionary
                instructions_dict[state] = instruction
                # Move the state one forward
                next_state = state

        # Create ratings list
        ratings_list = []
        # Go through each rating and split the thresholds
        for rating in ratings:
            x, m, a, s = rating.split(',')
            ratings_list.append([int(x[3:]), int(m[2:]), int(a[2:]), int(s[2:-1])])

    return instructions_dict, ratings_list


def check_acceptance(rating, instructions):
    # Initialize at the 'in' state
    state = 'in'
    # While we haven't reached one of the conclusive states
    while state not in ('A', 'R'):
        # Get the instruction details
        idx, value, lesser, greater = instructions[state]
        # Compare the relevant rating and decide which is our next state
        if rating[idx] >= value:
            state = greater
        else:
            state = lesser
    # Once we found a target state, we true or falls if the current rating was accepted
    return state == 'A'


def count_solutions(state, ranges, inst):
    # If we have a rejected state, we have no valid combinations for these ranges
    if state == 'R':
        return 0

    # Else if we have an accepted state, we can calculate the total combinations
    elif state == 'A':
        product = 1
        # The total combinations is just the range widths multiplied with each other
        for (lo, hi) in ranges:
            product *= (hi - lo)
        return product

    # Else we need to continue instructions
    else:
        # Get the next instruction details
        idx, value, lesser, greater = inst[state]
        # Get the low and high of the currently impacted range
        lo, hi = ranges[idx]

        # If the value is higher than our current high, we are fully in the lesser case and need to continue there
        if value >= hi:
            return count_solutions(lesser, ranges, inst)

        # Else if the value is smaller than our current low, we are fully in the greater case and need to continue there
        elif value <= lo:
            return count_solutions(greater, ranges, inst)

        # Else, we are somewhere in the middle and need to split our ranges, we always take the 'untouched' ranges with
        # us, but split the impacted one in two different parts. For low to the value, we have a lesser case, for value
        # to high, we have a greater case
        else:
            return count_solutions(lesser, ranges[:idx] + [(lo, value)] + ranges[idx + 1:], inst) +\
                count_solutions(greater, ranges[:idx] + [(value, hi)] + ranges[idx + 1:], inst)


# Solves part 1
def part_one(inst: dict, ratings: list) -> int:
    total = 0
    for rating in ratings:
        if check_acceptance(rating, inst):
            total += sum(rating)
    return total


# Solves part 2
def part_two(inst: dict) -> int:
    # Initialize count with full ranges
    total = count_solutions('in', [(1, 4001)] * 4, inst)
    return total


def main():
    inst, ratings = get_input()
    print('Adding together all of the rating numbers that ultimately get accepted yields:', part_one(inst, ratings))
    print("This many distinct combinations of ratings will be accepted by the Elves' workflows:", part_two(inst))


if __name__ == '__main__':
    main()
