from collections import deque


# Get data from .txt file
def get_input() -> list:
    with open('input/Day22.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize list of bricks
        bricks = []
        for line in data:
            # Brick will be of the form (x1, y1, z1, x2, y2, z2)
            bs, be = line.split('~')
            bs = list(map(int, bs.split(',')))
            be = list(map(int, be.split(',')))
            bricks.append(bs + be)
    return bricks


def overlap_xy(brick_a, brick_b):
    # Unpack the edge coordinates of each brick
    (x1_a, y1_a, _, x2_a, y2_a, _) = brick_a
    (x1_b, y1_b, _, x2_b, y2_b, _) = brick_b

    # Check for overlap in the X dimension
    overlap_x = max(x1_a, x1_b) <= min(x2_a, x2_b)

    # Check for overlap in the Y dimension
    overlap_y = max(y1_a, y1_b) <= min(y2_a, y2_b)

    return overlap_x and overlap_y


def fall_bricks(bricks: list) -> tuple[dict, dict]:
    # Assuming the first part of the brick is always lower, we can sort the bricks by z1
    bricks.sort(key=lambda x: x[2])
    # Move bricks down as far as possible
    for index, brick in enumerate(bricks):
        z2 = 1
        # Compare the brick to all other lower bricks
        for lower_bricks in bricks[:index]:
            # If they overlap in the x/y plane, z needs to be adjusted
            if overlap_xy(brick, lower_bricks):
                z2 = max(z2, lower_bricks[5] + 1)
            # Adjust the brick's z coordinates
            brick[5] = brick[5] - brick[2] + z2
            brick[2] = z2

    # After lowering all bricks, we need to sort again
    bricks.sort(key=lambda x: x[2])

    # Check which other bricks support the current brick and which other bricks the current brick supports
    support_to = {i: set() for i in range(len(bricks))}
    supported_by = {i: set() for i in range(len(bricks))}

    # Go through the bricks
    for j, upper in enumerate(bricks):
        # Get all bricks that are lower than the current one --> could be supporting bricks
        for i, lower in enumerate(bricks[:j]):
            # If the bricks overlap in x/y and their z is adjacent, then they connect
            if overlap_xy(lower, upper) and upper[2] == lower[5] + 1:
                # The lower one gives support to the upper one
                support_to[i].add(j)
                # The upper one is supported by the lower one
                supported_by[j].add(i)

    return support_to, supported_by


# Solves part 1
def part_one(bricks: list) -> int:
    # Get dicts of support
    support_to, supported_by = fall_bricks(bricks)
    # Initially we assume, you can remove all bricks
    total = len(bricks)
    # Go through each brick
    for i in range(len(bricks)):
        # For the current brick, check which other bricks it supports
        for j in support_to[i]:
            # Check if these other bricks have at least another support, if not, reduce the total and break
            if len(supported_by[j]) < 2:
                total -= 1
                break  # Exit the inner loop as soon as one condition fails
    return total


# Solves part 2
def part_two(bricks: list) -> int:
    # Get dicts of support
    support_to, supported_by = fall_bricks(bricks)
    # Initialize total list
    total_list = []
    # Go through each brick and check how many other it will make fall
    for i in range(len(bricks)):
        # Get all the supported bricks of the current brick and iterate through them to check, if that was the only
        # support. If yes, they are a falling brick.
        falling = set(filter(lambda x: len(supported_by[x]) == 1, support_to[i]))
        # Initialize queue with that set
        q = deque(falling)
        # Iterate through queue
        while q:
            # Get the next falling brick
            falling_brick = q.popleft()
            # Check which bricks it supported, these are now also potentially falling. Only add ones we haven't checked
            # already (the initial one cannot be it as well, it was disintegrated)
            new_falling_candidates = support_to[falling_brick] - falling - {i}
            # Go through all of these new falling bricks
            for new_falling_candidate in new_falling_candidates:
                # Check if all bricks that support the falling candidate are already falling (are a subset of the
                # falling set), this brick is now also falling, and we add it to the queue and falling bricks set
                if supported_by[new_falling_candidate] <= falling:
                    q.append(new_falling_candidate)
                    falling.add(new_falling_candidate)

        # Append to total falling list
        total_list.append(len(falling))
    # Return the sum of all totals
    return sum(total_list)


def main():
    print('This many bricks could be safely chosen as the one to get disintegrated:', part_one(get_input()))
    print('The sum of the number of other bricks that would fall is:', part_two(get_input()))


if __name__ == '__main__':
    main()
