import numpy as np
from heapq import heappush, heappop


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day17.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize array
        array = np.zeros((len(data), len(data[0])), dtype='int')
        # Create array
        for i, line in enumerate(data):
            array[i, :] = list(line)
    return array


# Solves part 1
def part_one(data: np.ndarray) -> int:
    # Get shape, only one direction required (square)
    n, m = data.shape
    # Dictionary of directions
    d_dict = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    # Initialize heat loss
    h_min = float('inf')
    # Starting positions
    pq = [(0, 0, 0, 'E', 0), (0, 0, 0, 'S', 0)]
    visited = set()
    # Go through queue
    while pq:
        h, y, x, d, count = heappop(pq)

        # If we are at the end position, we found our solution, update heat loss and break. Because we use the heap,
        # we can be certain that the first time we reach it, it's the optimal solution
        if y == n - 1 and x == m - 1:
            h_min = h
            break

        # If we have seen this state, skip it
        if (y, x, d, count) in visited:
            continue

        # Add the new state to visited
        visited.add((y, x, d, count))

        # If we have a count less than 3, move one more step in the same direction
        if count < 3:
            y_new = y + d_dict[d][0]
            x_new = x + d_dict[d][1]
            # Check if we are still within the grid
            if 0 <= y_new < n and 0 <= x_new < m:
                # Add new state variables and add one step to the count
                heappush(pq, (h + data[y_new, x_new], y_new, x_new, d, count + 1))

        # We want to turn, check which direction we currently have and determine the new directions
        if d in ('N', 'S'):
            new_dirs = ['E', 'W']
        else:
            new_dirs = ['N', 'S']

        # For each new direction
        for d_new in new_dirs:
            y_new = y + d_dict[d_new][0]
            x_new = x + d_dict[d_new][1]
            # Check if we are still within the grid
            if 0 <= y_new < n and 0 <= x_new < m:
                # Add new state variables, step count starts at 1 again
                heappush(pq, (h + data[y_new, x_new], y_new, x_new, d_new, 1))
    return h_min


# Solves part 2
def part_two(data: np.ndarray) -> int:
    # Get shape, only one direction required (square)
    n, m = data.shape
    # Dictionary of directions
    d_dict = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    # Initialize heat loss
    h_min = float('inf')
    # Starting position
    pq = [(0, 0, 0, '', 0)]
    visited = set()
    # Go through queue
    while pq:
        h, y, x, d, count = heappop(pq)

        # If we are at the end position, and we have a valid step count, we found our solution, update heat loss and
        # break. Because we use the heap, we can be certain that the first time we reach it, it's the optimal solution
        if y == n - 1 and x == m - 1 and count >= 4:
            h_min = h
            break

        # If we have seen this state, skip it
        if (y, x, d, count) in visited:
            continue

        # Add the new state to visited
        visited.add((y, x, d, count))

        # If we have a count less than 10, and we are not at the start, move one more step in the same direction
        if count < 10 and d != '':
            y_new = y + d_dict[d][0]
            x_new = x + d_dict[d][1]
            # Check if we are still within the grid
            if 0 <= y_new < n and 0 <= x_new < m:
                # Add new state variables and add one step to the count
                heappush(pq, (h + data[y_new, x_new], y_new, x_new, d, count + 1))

        # If we made our 4 steps, or we are at the start, we are allowed to turn
        if count >= 4 or d == '':
            # Get new directions
            if d in ('N', 'S'):
                new_dirs = ['E', 'W']
            elif d in ('E', 'W'):
                new_dirs = ['N', 'S']
            else:
                new_dirs = ['N', 'E', 'S', 'W']
            # For each new direction
            for d_new in new_dirs:
                y_new = y + d_dict[d_new][0]
                x_new = x + d_dict[d_new][1]
                # Check if we are still within the grid
                if 0 <= y_new < n and 0 <= x_new < m:
                    # Add new state variables, step count starts at 1 again
                    heappush(pq, (h + data[y_new, x_new], y_new, x_new, d_new, 1))
    return h_min


def main():

    print('The least heat loss it can incur is:', part_one(get_input()))
    print('The least heat loss it can incur is:', part_two(get_input()))


if __name__ == '__main__':
    main()
