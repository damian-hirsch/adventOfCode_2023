import numpy as np


# Get data from .txt file
def get_input() -> list:
    with open('input/Day13.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize variables
        array_list = []
        array = []
        # Check each line
        for line in data:
            # If we have a blank line, we finished an array and start a new one
            if line == '':
                # Convert list array to numpy array
                array = np.array(array)
                # Append array to our array list
                array_list.append(array)
                # Clear current array list
                array = []
            # Else, append line to array list and split the string
            else:
                array.append(list(line))
        # Convert and add the last array of the input (no blank line)
        array = np.array(array)
        array_list.append(array)
    return array_list


def check_mirror_part1(array: np.ndarray) -> int:
    # Go through rows and check combinations
    for j in range(1, array.shape[0]):
        # Get the stuff above the current row divider
        top = array[:j, :]
        # Get bottom part
        bot = array[j:, :]
        # Flip top around, so we can compare later, also makes it very simple to slice it
        top = np.flip(top, axis=0)
        # Make sure, our arrays have the same number of rows
        top = top[:bot.shape[0], :]
        bot = bot[:top.shape[0], :]

        # Check if the two arrays are the same
        is_horizontal_mirror = np.array_equal(top, bot)

        # If they are the same, return the row number
        if is_horizontal_mirror:
            # Return current row
            return j
    # Return 0 for no match
    return 0


def check_mirror_part2(array: np.ndarray) -> int:
    # Go through rows and check combinations
    for j in range(1, array.shape[0]):
        # Get the stuff above the current row divider
        top = array[:j, :]
        # Get bottom part
        bot = array[j:, :]
        # Flip top around, so we can compare later, also makes it very simple to slice it
        top = np.flip(top, axis=0)
        # Make sure, our arrays have the same number of rows
        top = top[:bot.shape[0], :]
        bot = bot[:top.shape[0], :]

        # Calculate the number of mismatches between 'top' and 'bot'
        mismatches = np.sum(top != bot)

        # Check if there is exactly one mismatch
        if mismatches == 1:
            # Return current row
            return j
    # Return 0 if there is no single mismatch
    return 0


# Solves part 1
def part_one(array_list: list) -> int:
    result = 0
    # Go through each array
    for array in array_list:
        # Check horizontal
        row = check_mirror_part1(array)
        # Multiply horizontal mirrors by 100
        result += row * 100

        # Check vertical by transposing the array to turn it into a horizontal check again
        col = check_mirror_part1(array.T)
        # Multiply vertical mirrors by 100
        result += col
    return result


# Solves part 2
def part_two(array_list: list) -> int:
    result = 0
    # Go through each array
    for array in array_list:
        # Check horizontal
        row = check_mirror_part2(array)
        # Multiply horizontal mirrors by 100
        result += row * 100

        # Check vertical by transposing the array to turn it into a horizontal check again
        col = check_mirror_part2(array.T)
        # Multiply vertical mirrors by 100
        result += col
    return result


def main():

    print('After summarizing all notes you get:', part_one(get_input()))
    print('After summarizing all notes with the new reflection line you get:', part_two(get_input()))


if __name__ == '__main__':
    main()
