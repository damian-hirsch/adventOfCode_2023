import numpy as np


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day14.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        array = np.zeros((len(data), len(data[0])), dtype='<U1')
        for i, line in enumerate(data):
            array[i, :] = list(line)
    return array


def calc_load(data: np.ndarray) -> int:
    total = 0
    # Go through each column
    n, m = data.shape
    for i in range(m):
        # Go through each row
        for j in range(n):
            # If we have a rounded rock, add its load
            if data[j, i] == 'O':
                total += n - j
    return total


# Solves part 1
def part_one(data: np.ndarray) -> int:
    total = 0
    # Go through each column
    n, m = data.shape
    for i in range(m):
        # Initialize column load
        counter = n
        # Go through each row to calculate dynamic load (rocks still need to move)
        for j in range(n):
            # If we have a rounded rock, add the current load and reduce it by 1
            if data[j, i] == 'O':
                total += counter
                counter -= 1
            # If we have a cubed rock, the load can now only be 1 less than that rock
            elif data[j, i] == '#':
                counter = n - j - 1
    return total


# Solves part 2
def part_two(data: np.ndarray, cycles: int) -> int:
    # Get shape
    n, m = data.shape
    # Initialize seen list (would be better to have a set, but then we cannot index it, which is needed later)
    # Convert data to hashable format
    seen = [data.tobytes()]
    # Start cycles
    for cycle in range(cycles):
        # Turn in all directions
        for _ in range(4):
            # Initialize new array of '.'
            new_data = np.full((n, m), '.', dtype='<U1')
            # Go through each column
            for i in range(m):
                # Initialize position in column
                pos = 0
                for j in range(n):
                    # If we find a rounded rock, move it to the currently lowest, possible position
                    if data[j, i] == 'O':
                        new_data[pos, i] = 'O'
                        # Increase position in column
                        pos += 1
                    # If we find a cubed rock
                    elif data[j, i] == '#':
                        # Leave it at its current position
                        new_data[j, i] = '#'
                        # Position in column is now after the cubed rock
                        pos = j + 1
            # Rotate the array clockwise and assign to data
            data = np.rot90(new_data, -1)

        # Check if data is already in seen
        if data.tobytes() in seen:
            # Get the index of the first occurrence
            fo = seen.index(data.tobytes())
            # Calculate the projected index where we would be at 1000000000 cycles
            projected_index = (cycles - fo) % (cycle + 1 - fo) + fo
            # Recreate the array from bytes
            data = np.frombuffer(seen[projected_index], dtype='<U1').reshape(n, m)
            break
        # If not seen, append it
        else:
            seen.append(data.tobytes())
    # Calculate the static load (rocks have already moved)
    return calc_load(data)


def main():

    print('The total load on the north support beams is:', part_one(get_input()))
    print('The total load on the north support beams is:', part_two(get_input(), 1000000000))


if __name__ == '__main__':
    main()
