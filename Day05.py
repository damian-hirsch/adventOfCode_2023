# Get data from .txt file
def get_input() -> (list, list[list]):
    with open('input/Day05.txt', 'r') as file:
        # Splitlines
        data = file.read().splitlines()
        # Get seed values
        seeds = data[0].split(': ')[1]
        seeds = list(map(int, seeds.split()))
        # Remove seed part
        data = data[2:]
        mapper_list = []
        mapper = []
        # Create mappers for each instruction
        for line in data:
            # If we find a blank line, we know the last instruction is finished and move to the next
            if line == '':
                mapper_list.append(mapper)
                mapper = []
            # If we have a letter, we have an instruction name, which is irrelevant
            elif line[0].isalpha():
                continue
            # If we have a digit, we have a mapper
            elif line[0].isdigit():
                numbers = list(map(int, line.split()))
                # Convert the mapper to (range start, range end, correction value)
                mapper.append((numbers[1], numbers[1] + numbers[2], numbers[0] - numbers[1]))
        # Add last instruction when done
        else:
            mapper_list.append(mapper)
    return seeds, mapper_list


# Solves part 1
def part_one(seeds: list, mapper_list: list[dict]) -> int:
    # Initialize results seed list
    seed_list = []
    for seed in seeds:
        # Go through all instructions
        for mappers in mapper_list:
            # Go through each mapper of each instruction
            for mapper in mappers:
                # Check if a seed is in range of a mapper
                if seed in range(mapper[0], mapper[1]):
                    # If yes, add correction value and break
                    seed = seed + mapper[2]
                    break
                else:
                    # Else, nothing changes (numbers stay the same)
                    continue
        seed_list.append(seed)
    # Return smallest seed
    return min(seed_list)


# Solves part 2
def part_two(seeds: list, mapper_list: list[dict]) -> int:
    # Convert seeds to ranges
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    # For performance reasons, we need to handle everything in ranges (otherwise there are too many seeds), thus we need
    # to go through the mapper in ranges and compare them to each other
    for mappers in mapper_list:
        new_seed_ranges = []
        # Loop until we are out of ranges (new ones can be created)
        while len(seed_ranges) > 0:
            # Pop one seed range and get start and end value
            seed_start, seed_end = seed_ranges.pop()
            # Go through each mapper of each instruction
            for mapper in mappers:
                # Check if there are overlaps
                overlap_start = max(seed_start, mapper[0])
                overlap_end = min(seed_end, mapper[1])
                # If overlap_start is smaller than overlap_end, we have an overlap
                if overlap_start < overlap_end:
                    # Create the new seed ranges by adjusting with the correction value
                    new_seed_ranges.append((overlap_start + mapper[2], overlap_end + mapper[2]))
                    # We also need to look at all edges, if our overlap only partial covers the range
                    # We only need to consider cases, where not the whole seed range has been used, the mapper range is
                    # irrelevant because if there are no seeds, there is no impact
                    # Check if there is a seed range on the left that hasn't been covered and add it back to the
                    # original seed ranges to check further
                    if overlap_start > seed_start:
                        seed_ranges.append((seed_start, overlap_start))
                    # Check and do the same but on the right of the overlap
                    if overlap_end < seed_end:
                        seed_ranges.append((overlap_end, seed_end))
                    break
            else:
                # If there was no overlap at all, we can just add the same range again
                new_seed_ranges.append((seed_start, seed_end))
        # One we are done with the current instruction, we set the current seed_ranged to the new_seed_ranges and repeat
        seed_ranges = new_seed_ranges
    # Find the lowest range and take it's starting seed which will be the lowest seed overall
    return min(seed_ranges)[0]


def main():
    seeds, mapper_list = get_input()
    print('The lowest location number that corresponds to any of the initial seeds is:', part_one(seeds, mapper_list))
    print('The lowest location number that corresponds to any of the initial seeds is:', part_two(seeds, mapper_list))


if __name__ == '__main__':
    main()
