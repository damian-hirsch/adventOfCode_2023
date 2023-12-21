import numpy as np
from heapq import heappush, heappop


# Get data from .txt file
def get_input() -> tuple[np.ndarray, tuple[int, int]]:
    with open('input/Day21.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize array
        array = np.zeros((len(data), len(data[0])), dtype='<U1')
        start = (None, None)
        # Create array
        for i, line in enumerate(data):
            # Replace 'S' with a '.'
            if 'S' in line:
                index = line.index('S')
                start = (i, index)
                line = line[:index] + '.' + line[index + 1:]
            array[i, :] = list(line)
    return array, start


# Solves part 1
def part_one(array: np.ndarray, start: tuple, steps: int) -> int:
    # Get shape, only one direction required (square)
    n, m = array.shape
    # Dictionary of directions
    directions = {(-1, 0), (0, 1), (1, 0), (0, -1)}
    # Starting positions, queue initialized as (num_steps, (y, x))
    pq = [(steps, start)]
    # Initialize visited and solutions sets
    visited = set()
    solutions = set()
    # Go through queue
    while pq:
        num_steps, pos = heappop(pq)

        # Check if we are out of steps, then this is a solution
        if num_steps == 0:
            solutions.add(pos)
            continue

        # Add the new state to visited
        visited.add((num_steps, pos))

        # Check each direction
        for direction in directions:
            y_new = pos[0] + direction[0]
            x_new = pos[1] + direction[1]
            # Check if direction is valid: within the grid, not blocked, and not already visited
            if 0 <= y_new < n and 0 <= x_new < m and array[y_new, x_new] != '#'\
                    and (num_steps - 1, (y_new, x_new)) not in visited:
                heappush(pq, (num_steps - 1, (y_new, x_new)))

    return len(solutions)


# Solves part 2: The hard part of this one is to realize, that the steps are perfectly in sync with the grid and divide
# nicely into steps = x * n + n//2. Looking at the results of a few test and a bit of luck, one can get that the results
# in sync with these grid, follow a quadratic polynomial of the form a0 + a1*x + a2*x**2. We can then use a Newton
# polynomial of the form a0 + a1*(x - x0) + a2*(x - x0)*(x -x1) where (x0, y0), (x1, y1), (x2, y2) are inputs and
# solutions to solve the problem.
# Note: Changes part two to a different code, because this runs quite a bit faster (fewer checks).
def part_two(array: np.ndarray, start: tuple, steps: int) -> int:
    # Get size
    n, m = array.shape
    # Dictionary of directions
    directions = {(-1, 0), (0, 1), (1, 0), (0, -1)}
    # Initialize visited and solutions sets
    solutions = {start}
    # Initialize solutions
    ys = [0, 0, 0]
    # Step factor
    step_factor = 0
    # Go through queue
    for step_count in range(1, steps):
        new_solutions = set()
        # Advance each solution from the last step
        for pos in solutions:
            # Check each direction
            for direction in directions:
                y_new = pos[0] + direction[0]
                x_new = pos[1] + direction[1]
                # Check if the position is not blocked and add to new solutions
                if array[y_new % n, x_new % m] != '#':
                    new_solutions.add((y_new, x_new))
        # Reassign new solutions
        solutions = new_solutions
        # Collection solutions at steps n//2, n//2 + n, n//2 + 2*n
        if step_count == n//2 + n * step_factor:
            ys[step_factor] = len(solutions)
            step_factor += 1
            # Once we have y0, y1, y2, we can break and calculate the result
            if step_factor >= 3:
                break

    # Calculating constants of polynomial
    a0 = ys[0]
    a1 = (ys[1] - ys[0]) / n
    a2 = (ys[2] - 2 * ys[1] + ys[0]) / (2 * n ** 2)
    # Calculating result
    ans = a0 + a1 * (steps - n//2) + a2 * (steps - n//2) * (steps - n - n//2)
    return int(ans)


def main():
    array, start = get_input()
    print('This many garden plots could the Elf reach in exactly 64 steps:', part_one(array, start, 64))
    print('This many garden plots could the Elf reach in exactly 26501365 steps:', part_two(array, start, 26501365))


if __name__ == '__main__':
    main()
