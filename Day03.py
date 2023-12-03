import string
import numpy as np


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day03.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read().splitlines()
        # Splitting each string into characters and creating a 2D array
        schematic = np.array([list(character) for character in data])
    return schematic


def check_neighbors(data: np.ndarray, y: int, x: int, symbols: set) -> bool:
    # Get array shape
    y_len, x_len = data.shape
    # N, NE, E, SE, S, SW, W, NW
    check_directions = {(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)}
    # Get all neighboring positions
    neighbors = [(y + d[0], x + d[1]) for d in check_directions]
    # Check all neighbors
    for neighbor in neighbors:
        # Check if valid neighbor and if it has a symbol
        if 0 <= neighbor[0] <= y_len - 1 and 0 <= neighbor[1] <= x_len - 1 and data[neighbor[0], neighbor[1]] in symbols:
            return True
    return False


def get_neighbors_digits(data: np.ndarray, y: int, x: int, digits: set) -> int:
    # Initialize candidates
    candidates = set()
    # Get array shape
    y_len, x_len = data.shape
    # N, NE, E, SE, S, SW, W, NW
    check_directions = {(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)}
    # Get all neighboring positions
    neighbors = [(y + d[0], x + d[1]) for d in check_directions]
    # Check all neighbors
    for neighbor in neighbors:
        # Check if neighbor is a digit
        if 0 <= neighbor[0] <= y_len - 1 and 0 <= neighbor[1] <= x_len - 1 and data[neighbor[0], neighbor[1]] in digits:
            # If it is a digit, backtrace it until the beginning and save that position
            back_trace = 0
            while neighbor[1] - back_trace >= 0 and data[neighbor[0], neighbor[1] - back_trace] in digits:
                back_trace += 1
            # Add position to set (double counts will be omitted this way)
            candidates.add((neighbor[0], neighbor[1] - back_trace + 1))

    # If we have only one candidate, we cannot have a gear ratio
    if len(candidates) != 2:
        return 0

    # For each candidate, get its number
    numbers = []
    for candidate in candidates:
        # Trace forward as long as we encounter digits, update the number accordingly
        front_trace = 0
        number = 0
        while candidate[1] + front_trace < x_len and data[candidate[0], candidate[1] + front_trace] in digits:
            number = number * 10 + int(data[candidate[0], candidate[1] + front_trace])
            front_trace += 1
        numbers.append(number)
    # Multiply gear ratio
    return numbers[0] * numbers[1]


# Solves part 1
def part_one(data: np.ndarray) -> int:
    # Get Symbols
    mask = ~np.char.isdecimal(data) & (data != '.')
    symbols = set(data[mask])
    # Initialize variables
    total = 0
    # Get array shape
    y, x = data.shape
    # Go through all entries
    for j in range(0, y):
        number = 0
        has_symbol = False
        for i in range(0, x):
            # Check if it is a digit
            if data[j, i].isdigit():
                # Update number
                number = number * 10 + int(data[j, i])
                # Check if it has a symbol around (use or operator to ensure we don't overwrite a previously seen one)
                has_symbol = check_neighbors(data, j, i, symbols) or has_symbol
            # If we don't have a digit or at the end of the row, add the current number to the total and reset
            if not data[j, i].isdigit() or i == x - 1:
                if has_symbol:
                    total += number
                number = 0
                has_symbol = False
    return total


# Solves part 2
def part_two(data: np.ndarray) -> int:
    # Initialize variables
    total = 0
    digits = set(string.digits)
    # Get array shape
    y, x = data.shape
    # Go through all entries
    for j in range(0, y):
        for i in range(0, x):
            # If the current entry is not a * and no neighbors have digits, continue
            if data[j, i] != '*' or not check_neighbors(data, j, i, digits):
                continue
            # Else get the neighboring digits and return the result
            else:
                total += get_neighbors_digits(data, j, i, digits)
    return total


def main():

    print('The sum of all of the part numbers in the engine schematic is:', part_one(get_input()))
    print('The sum of all of the gear ratios in your engine schematic is:', part_two(get_input()))


if __name__ == '__main__':
    main()
