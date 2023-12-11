import numpy as np


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day11.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize np array
        observed = np.full((len(data), len(data[0])), '', dtype='<U1')
        # Fill the np array
        for i, line in enumerate(data):
            observed[i, :] = list(line)
    return observed


# Solves part 1 and part 2
def part_one_and_two(data: np.ndarray, scale: int) -> int:
    # Check if all elements in each row are equal to '.'
    all_dots_per_row = np.all(data == '.', axis=1)
    # Check if all elements in each column are equal to '.'
    all_dots_per_column = np.all(data == '.', axis=0)

    # List to store the positions of '#'
    positions = []

    # Iterate through each element in the array
    for j in range(data.shape[0]):  # Loop over rows
        # Correction value depending on how many empty rows we have
        y_correction = (scale - 1) * sum(all_dots_per_row[:j])
        for i in range(data.shape[1]):  # Loop over columns
            # Correction value depending on how many empty columns we have
            x_correction = (scale - 1) * sum(all_dots_per_column[:i])
            # Check if we have a galaxy
            if data[j, i] == '#':
                # Add position with corrected for the spacing
                positions.append((j + y_correction, i + x_correction))

    # Check all combinations and calculate distances
    distances = []
    for position_1 in positions:
        for position_2 in positions:
            distances.append(abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1]))

    # Because we also have the reverse combination, we need to divide by 2
    return sum(distances) // 2


def main():

    print('The sum of these lengths is:', part_one_and_two(get_input(), 2))
    print('The sum of these lengths is:', part_one_and_two(get_input(), 1000000))


if __name__ == '__main__':
    main()
