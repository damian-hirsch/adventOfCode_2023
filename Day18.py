import numpy as np


# Get data from .txt file
def get_input() -> tuple:
    with open('input/Day18.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize lists
        directions = []
        nums = []
        colors = []
        # Split line and appends to respective lists
        for line in data:
            direction, num, color = line.split()
            directions.append(direction)
            nums.append(int(num))
            colors.append(color[1:-1])
    return directions, nums, colors


# [old] Iterative flood fill algorithm (similar to day 10 part 2)
def flood_fill_iterative(array, y, x, target):
    # Initialize stack
    stack = [(y, x)]

    # While there are locations in stack
    while stack:
        y, x = stack.pop()

        # Check if we are within bounds
        if y < 0 or y >= array.shape[0] or x < 0 or x >= array.shape[1]:
            continue

        # If it's not '.', it's already flooded
        if array[y, x] != target:
            continue

        # Else, mark it as '#'
        array[y, x] = '#'  # Marking as '#'

        # Add neighboring cells to the stack
        stack.append((y + 1, x))
        stack.append((y - 1, x))
        stack.append((y, x + 1))
        stack.append((y, x - 1))


# [old] Solves part 1
def part_one_old(directions: list, nums: list) -> int:
    # Initialize current location
    current = (0, 0)
    coords = {current}
    # Go through instructions
    for i, direction in enumerate(directions):
        # Depending on direction, add coordinates respectively
        match direction:
            case 'U':
                for j in range(nums[i]):
                    current = (current[0] - 1, current[1])
                    coords.add(current)
            case 'R':
                for j in range(nums[i]):
                    current = (current[0], current[1] + 1)
                    coords.add(current)
            case 'D':
                for j in range(nums[i]):
                    current = (current[0] + 1, current[1])
                    coords.add(current)
            case 'L':
                for j in range(nums[i]):
                    current = (current[0], current[1] - 1)
                    coords.add(current)

    # Find minimum y and x values in coordinates
    min_y = min(coord[0] for coord in coords)
    min_x = min(coord[1] for coord in coords)

    # Offset all coordinates so that the minimum value starts at 0
    adjusted_coordinates = [(y - min_y, x - min_x) for y, x in coords]

    # Determine the size of the array
    max_y = max(coord[0] for coord in adjusted_coordinates) + 1
    max_x = max(coord[1] for coord in adjusted_coordinates) + 1

    # Create an array filled with a placeholder, e.g., '.'
    array = np.full((max_y, max_x), '.')

    # Place '#' at the adjusted coordinates
    for y, x in adjusted_coordinates:
        array[y, x] = '#'

    # Flood fill from the edges
    for i in range(array.shape[0]):
        # Left edge
        flood_fill_iterative(array, i, 0, '.')
        # Right edge
        flood_fill_iterative(array, i, array.shape[1] - 1, '.')

    for j in range(array.shape[1]):
        # Top edge
        flood_fill_iterative(array, 0, j, '.')
        # Bottom edge
        flood_fill_iterative(array, array.shape[0] - 1, j, '.')

    # The length of the original digging spots plus the ones that are enclose (remain '.') is the lagoon size
    return len(coords) + np.sum(array == '.')


def calc_area(directions: list, nums: list) -> int:
    # Initialize starting spot
    total = 1
    length = 1
    # Go through all instructions
    for i, direction in enumerate(directions):
        # Here we are summing up areas going up (plus) or down (minus), while left and right adjust the lengths
        match direction:
            # Going up means, we are subtracting from our area, so we need subtract from it (note that the trench path
            # itself is also counted as area, thus we need to add -1 to the length)
            case 'U':
                total -= (length - 1) * nums[i]
            # Going right means we are extending our area length, we also need to add the added trenches themselves
            case 'R':
                length += nums[i]
                total += nums[i]
            # Going down means we are creating an area, so we need to add it to our total
            case 'D':
                total += length * nums[i]
            # Going left means we are reducing our area length, we don't subtract the trench itself, because it is still
            # a trench
            case 'L':
                length -= nums[i]
    return total


# Solves part 1
def part_one(directions: list, nums: list) -> int:
    # Calculate the area
    return calc_area(directions, nums)


# Solves part 2
def part_two(colors: list) -> int:
    real_nums = []
    real_dirs = []
    dirs_dict = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    # Convert values using hex conversion with integer
    for color in colors:
        hex_val = '0x' + color[1:-1]
        real_nums.append(int(hex_val, 16))
        real_dirs.append(dirs_dict[color[-1]])
    # Calculate the area with the updated instructions
    return calc_area(real_dirs, real_nums)


def main():
    dirs, nums, colors = get_input()
    print('It could hold this many cubic meters of lava:', part_one(dirs, nums))
    print('It could hold this many cubic meters of lava:', part_two(colors))


if __name__ == '__main__':
    main()
