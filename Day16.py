import numpy as np
from collections import deque


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day16.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize array
        array = np.zeros((len(data), len(data[0])), dtype='<U1')
        # Create array
        for i, line in enumerate(data):
            array[i, :] = list(line)
    return array


def get_energized_tiles(data: np.ndarray, q: deque, visited: set) -> int:
    # Get shape, only one direction required (square)
    n = data.shape[0]
    # Dictionary of directions
    d_dict = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    # Go through queue
    while q:
        # Get last queue entry
        y, x, d = q.popleft()
        # Check its character at that position
        char = data[y, x]
        # Initialize new direction list
        new_d = []
        # Get next candidates
        match char:
            # If the char is a '.', the direction doesn't change
            case '.':
                new_d.append(d)
            # If the char is a '/', the direction changes accordingly
            case '/':
                match d:
                    case 'N':
                        new_d.append('E')
                    case 'E':
                        new_d.append('N')
                    case 'S':
                        new_d.append('W')
                    case 'W':
                        new_d.append('S')
            # If the char is a '\', the direction changes accordingly
            case '\\':
                match d:
                    case 'N':
                        new_d.append('W')
                    case 'E':
                        new_d.append('S')
                    case 'S':
                        new_d.append('E')
                    case 'W':
                        new_d.append('N')
            # If the char is a '-', the beam is split if it comes from the north or south, otherwise the direction remains
            case '-':
                match d:
                    case 'N':
                        new_d.append('W')
                        new_d.append('E')
                    case 'E':
                        new_d.append('E')
                    case 'S':
                        new_d.append('W')
                        new_d.append('E')
                    case 'W':
                        new_d.append('W')
            # If the char is a '|', the beam is split if it comes from the east or west, otherwise the direction remains
            case '|':
                match d:
                    case 'N':
                        new_d.append('N')
                    case 'E':
                        new_d.append('N')
                        new_d.append('S')
                    case 'S':
                        new_d.append('S')
                    case 'W':
                        new_d.append('N')
                        new_d.append('S')
        # Go through all new directions (if there was a beam splitter, we have two directions)
        for d in new_d:
            # Get new location
            new_y = y + d_dict[d][0]
            new_x = x + d_dict[d][1]
            # Check if it's in bound and if we didn't already visit it going in this direction
            if 0 <= new_y < n and 0 <= new_x < n and (new_y, new_x, d) not in visited:
                # Add to queue and visited
                visited.add((new_y, new_x, d))
                q.append((new_y, new_x, d))

    # Some locations can be in there up to 4 times (going in different directions), we filter those out
    energized = {(y, x) for (y, x, _) in visited}
    # Return the length of all visited locations
    return len(energized)


# Solves part 1
def part_one(data: np.ndarray) -> int:
    # Start top left going east
    visited = {(0, 0, 'E')}
    q = deque([(0, 0, 'E')])
    return get_energized_tiles(data, q, visited)


# Solves part 2
def part_two(data: np.ndarray) -> int:
    n = data.shape[0]
    energized = []
    # Go through all edges
    for i in range(n):
        # Top edge
        energized.append(get_energized_tiles(data, deque([(0, i, 'S')]), {(0, i, 'S')}))
        # Bottom edge
        energized.append(get_energized_tiles(data, deque([(n - 1, i, 'N')]), {(n - 1, i, 'N')}))
        # Left edge
        energized.append(get_energized_tiles(data, deque([(i, 0, 'E')]), {(i, 0, 'E')}))
        # Right edge
        energized.append(get_energized_tiles(data, deque([(i, n - 1, 'W')]), {(i, n - 1, 'W')}))
    # Return the largest value
    return max(energized)


def main():

    print('This many tiles end up being energized:', part_one(get_input()))
    print('This many tiles are energized in that configuration:', part_two(get_input()))


if __name__ == '__main__':
    main()
