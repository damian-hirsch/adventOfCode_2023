import numpy as np


# Get data from .txt file
def get_input() -> np.ndarray:
    with open('input/Day23.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize array
        array = np.zeros((len(data), len(data[0])), dtype='<U1')
        # Create array
        for i, line in enumerate(data):
            array[i, :] = list(line)
    return array


def get_branches(array: np.ndarray, dirs: dict) -> dict:
    # Get array shape
    n, m = array.shape
    # Initialize start and end
    start = (0, 1)
    end = (n-1, m-2)
    # Initialize branch points
    branches = [start, end]
    # Get branching positions
    for y in range(n):
        for x in range(m):
            # If we have a forest, it cannot be a branch position
            if array[y, x] == '#':
                continue
            else:
                num_neighbors = 0
                # Check in how many directions we can actually go
                for direction in dirs[array[y, x]]:
                    y_new = y + direction[0]
                    x_new = x + direction[1]
                    # Check if the direction is valid
                    if 0 <= y_new < n and 0 <= x_new < m and array[y_new, x_new] != '#':
                        num_neighbors += 1
                # If we have more than 2 directions, we have a path branch
                if num_neighbors > 2:
                    branches.append((y, x))

    # Initialize branch dictionary
    branch_dict = {branch: {} for branch in branches}

    # Calculate the actual path length from branch point to branch point (if it exists)
    for yb, xb in branches:
        stack = [(0, yb, xb)]
        visited = {(yb, xb)}

        while stack:
            steps, y, x = stack.pop()

            # If we are not in the initial step, and we found another branch
            if steps != 0 and (y, x) in branches:
                # Update branch dictionary and continue
                branch_dict[(yb, xb)][(y, x)] = steps
                continue

            # Take the next step
            for direction in dirs[array[y, x]]:
                y_new = y + direction[0]
                x_new = x + direction[1]
                # Make sure the new position is valid, and we haven't visited it yet
                if 0 <= y_new < n and 0 <= x_new < m and array[y_new, x_new] != '#' and (y_new, x_new) not in visited:
                    stack.append((steps + 1, y_new, x_new))
                    visited.add((y_new, x_new))
    return branch_dict


def dfs(branch: tuple, end: tuple, branch_dict: dict, visited: set):
    # If the branch is our target branch, we are done, 0 steps extra needed
    if branch == end:
        return 0

    # Initialize steps
    max_steps = -float('inf')

    # Add this branch to the visited branches
    visited.add(branch)
    # Compare this branch now to all other branches in the dictionary
    for new_branch in branch_dict[branch]:
        # If we haven't visited the new branch, and we have a valid path
        if new_branch not in visited:
            # Check how many steps we need from the new branch to the end and update the steps, compare to the current
            # max and take the larger
            max_steps = max(max_steps, dfs(new_branch, end, branch_dict, visited) + branch_dict[branch][new_branch])
    visited.remove(branch)

    return max_steps


# Solves part 1
def part_one(array: np.ndarray) -> int:
    # Start position
    start = (0, 1)
    # Get array shape for end position
    n, m = array.shape
    end = (n - 1, m - 2)
    # Define possible directions
    dirs = {
        '.': [(-1, 0), (0, 1), (1, 0), (0, -1)],
        '^': [(-1, 0)],
        '>': [(0, 1)],
        'v': [(1, 0)],
        '<': [(0, -1)]
    }
    # Get branch data
    branch_dict = get_branches(array, dirs)
    # Initialize visited set
    visited = set()
    # We now do a DFS over the branches instead of positions
    return dfs(start, end, branch_dict, visited)


# Solves part 2
def part_two(array: np.ndarray) -> int:
    # Start position
    start = (0, 1)
    # Get array shape for end position
    n, m = array.shape
    end = (n - 1, m - 2)
    # Define possible directions
    dirs = {
        '.': [(-1, 0), (0, 1), (1, 0), (0, -1)],
        '^': [(-1, 0), (0, 1), (1, 0), (0, -1)],
        '>': [(-1, 0), (0, 1), (1, 0), (0, -1)],
        'v': [(-1, 0), (0, 1), (1, 0), (0, -1)],
        '<': [(-1, 0), (0, 1), (1, 0), (0, -1)]
    }
    # Get branch data
    branch_dict = get_branches(array, dirs)
    # Initialize visited set
    visited = set()
    # We now do a DFS over the branches instead of positions
    return dfs(start, end, branch_dict, visited)


def main():

    print('The longest hike has this many steps:', part_one(get_input()))
    print('The longest hike has this many steps:', part_two(get_input()))


if __name__ == '__main__':
    main()
