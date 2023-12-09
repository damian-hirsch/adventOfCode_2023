# Get data from .txt file
def get_input() -> list:
    with open('input/Day09.txt', 'r') as file:
        # Split lines, and write each line to list
        data = file.read().splitlines()
        # Split each line into integers
        data = [list(map(int, line.split())) for line in data]
    return data


# Solves part 1
def part_one(data: list) -> int:
    total = 0
    for line in data:
        # Initialize with the original list
        difference_list = [line]
        # Check if the latest difference list has all zeros
        while not all(x == 0 for x in difference_list[-1]):
            # Create a new list with the differences and append to our difference list
            difference = [j - i for i, j in zip(difference_list[-1], difference_list[-1][1:])]
            difference_list.append(difference)
        # Once we found the list with all zeros
        else:
            new_result = 0
            # Cycle through backwards and add up the last entry to get the end result
            for difference in difference_list[::-1]:
                new_result += difference[-1]
            # Add result to total
            total += new_result
    return total


# Solves part 2
def part_two(data: list) -> int:
    total = 0
    for line in data:
        # Initialize with the original list
        difference_list = [line]
        # Check if the latest difference list has all zeros
        while not all(x == 0 for x in difference_list[-1]):
            # Create a new list with the differences and append to our difference list
            difference = [j - i for i, j in zip(difference_list[-1], difference_list[-1][1:])]
            difference_list.append(difference)
        # Once we found the list with all zeros
        else:
            new_result = 0
            # Cycle through backwards and subtract the current result from the first value in the list (only difference
            # to part 1)
            for difference in difference_list[::-1]:
                new_result = difference[0] - new_result
            # Add result to total
            total += new_result
    return total


def main():

    print('The sum of these extrapolated values is:', part_one(get_input()))
    print('The sum of these extrapolated values is:', part_two(get_input()))


if __name__ == '__main__':
    main()
