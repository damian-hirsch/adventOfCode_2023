from collections import deque


# Get data from .txt file
def get_input() -> tuple[list, int, int]:
    with open('input/Day10.txt', 'r') as file:
        # Remove space and split lines
        data = file.read().strip().splitlines()
        # Create grid
        for r, row in enumerate(data):
            for c, pipe in enumerate(row):
                if pipe == "S":
                    sr = r
                    sc = c
    return data, sr, sc


# Iterative flood fill algorithm (recursive version won't work, due to stack overflow)
def iterative_flood_fill(grid, x, y, visited):
    # Check if we are on a blocker, or we have visited it already
    if grid[x][y] == "#" or visited[x][y]:
        return 0

    # Initialize queue and count
    queue = deque([(x, y)])
    count = 0

    while queue:
        cx, cy = queue.popleft()
        # If visited, already accounted for
        if visited[cx][cy]:
            continue

        # Mark the cell as visited
        visited[cx][cy] = True

        # Count "X" in the current cell
        if grid[cx][cy] == "X":
            count += 1

        # Add adjacent cells to the queue
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = cx + dx, cy + dy
            # If the new cell is still within the grid, not visited, and not a blocker, add it to the queue
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not visited[nx][ny] and grid[nx][ny] != "#":
                queue.append((nx, ny))

    # Return the "X" count
    return count


# Solves part 1
def part_one(grid: list, sr: int, sc: int) -> int:
    visited = {(sr, sc)}
    queue = deque([(sr, sc)])
    while queue:
        r, c = queue.popleft()
        pipe = grid[r][c]

        # Go North
        if r > 0 and pipe in "S|JL" and grid[r - 1][c] in "|7F" and (r - 1, c) not in visited:
            visited.add((r - 1, c))
            queue.append((r - 1, c))
        # Go East
        if c < len(grid[r]) - 1 and pipe in "S-LF" and grid[r][c + 1] in "-J7" and (r, c + 1) not in visited:
            visited.add((r, c + 1))
            queue.append((r, c + 1))
        # Go South
        if r < len(grid) - 1 and pipe in "S|7F" and grid[r + 1][c] in "|LJ" and (r + 1, c) not in visited:
            visited.add((r + 1, c))
            queue.append((r + 1, c))
        # Go West
        if c > 0 and pipe in "S-J7" and grid[r][c - 1] in "-LF" and (r, c - 1) not in visited:
            visited.add((r, c - 1))
            queue.append((r, c - 1))

    return len(visited) // 2


# Solves part 2
def part_two(grid: list, sr: int, sc: int) -> int:
    visited = {(sr, sc)}
    queue = deque([(sr, sc)])
    while queue:
        r, c = queue.popleft()
        pipe = grid[r][c]

        # Go North
        if r > 0 and pipe in "S|JL" and grid[r - 1][c] in "|7F" and (r - 1, c) not in visited:
            visited.add((r - 1, c))
            queue.append((r - 1, c))
        # Go East
        if c < len(grid[r]) - 1 and pipe in "S-LF" and grid[r][c + 1] in "-J7" and (r, c + 1) not in visited:
            visited.add((r, c + 1))
            queue.append((r, c + 1))
        # Go South
        if r < len(grid) - 1 and pipe in "S|7F" and grid[r + 1][c] in "|LJ" and (r + 1, c) not in visited:
            visited.add((r + 1, c))
            queue.append((r + 1, c))
        # Go West
        if c > 0 and pipe in "S-J7" and grid[r][c - 1] in "-LF" and (r, c - 1) not in visited:
            visited.add((r, c - 1))
            queue.append((r, c - 1))

    # Deduce pipe type for starting point "S"
    # S is |
    if grid[sr - 1][sc] in "|7F" and grid[sr + 1][sc] in "|LJ":
        grid[sr] = grid[sr][:sc] + "|" + grid[sr][sc + 1:]
    # S is -
    elif grid[sr][sc - 1] in "-LF" and grid[sr][sc + 1] in "-J7":
        grid[sr] = grid[sr][:sc] + "-" + grid[sr][sc + 1:]
    # S is L
    elif grid[sr - 1][sc] in "|7F" and grid[sr][sc + 1] in "-J7":
        grid[sr] = grid[sr][:sc] + "L" + grid[sr][sc + 1:]
    # S is J
    elif grid[sr][sc - 1] in "-LF" and grid[sr - 1][sc] in "|7F":
        grid[sr] = grid[sr][:sc] + "J" + grid[sr][sc + 1:]
    # S is 7
    elif grid[sr][sc - 1] in "-LF" and grid[sr + 1][sc] in "|LJ":
        grid[sr] = grid[sr][:sc] + "7" + grid[sr][sc + 1:]
    # S is F
    elif grid[sr + 1][sc] in "|LJ" and grid[sr][sc + 1] in "-J7":
        grid[sr] = grid[sr][:sc] + "F" + grid[sr][sc + 1:]

    # Replace all not used parts with .
    new_grid = []  # This will store the new grid
    # Iterate over each row in the grid with its index
    for r, row in enumerate(grid):
        new_row = ""  # Start with an empty string for the new row
        # Iterate over each character in the row with its index
        for c, ch in enumerate(row):
            # Check if the current position is in the visited set
            if (r, c) in visited:
                new_row += ch  # If visited, keep the original character
            else:
                new_row += "."  # If not visited, replace with "."
        new_grid.append(new_row)
    grid = new_grid

    # Build new, bigger grid, where # is the metal pipe, and . free space to move along it. Add X to still being able to
    # differentiate free spaces.
    large_grid_dict = {
        ".": ["...", ".X.", "..."],
        "|": [".#.", ".#.", ".#."],
        "-": ["...", "###", "..."],
        "L": [".#.", ".##", "..."],
        "J": [".#.", "##.", "..."],
        "7": ["...", "##.", ".#."],
        "F": ["...", ".##", ".#."],
    }

    # Rebuild the grid
    large_grid = []
    for r in grid:
        # Create a buffer for 3 rows for each character row
        new_rows = ["", "", ""]
        for char in r:
            # Expand each character to 3x3
            expanded_char = large_grid_dict[char]
            # Append each row of expanded character to the corresponding new row
            for i in range(3):
                new_rows[i] += expanded_char[i]
        # Add the new rows to the new grid
        large_grid.extend(new_rows)

    # Count reachable "X"
    m, n = len(large_grid), len(large_grid[0])
    # Create visited grid of bools
    visited = [[False for _ in range(n)] for _ in range(m)]
    # Get total Xs
    total_x_count = sum(row.count("X") for row in large_grid)

    reachable_x_count = 0

    # Start iterative flood fill from the edges of the grid (required to avoid pipes blocking a path that still connects
    # to the outside)
    # Left edge
    for r in range(m):
        if not visited[r][0]:
            reachable_x_count += iterative_flood_fill(large_grid, r, 0, visited)
    # Top edge
    for c in range(n):
        if not visited[0][c]:
            reachable_x_count += iterative_flood_fill(large_grid, 0, c, visited)

    # The total count of not reachable Xs is the total minus the reachable ones
    return total_x_count - reachable_x_count


def main():
    print("It takes this many steps to get from the start to the farthest position:", part_one(*get_input()))
    print("This many tiles are enclosed by the loop:", part_two(*get_input()))


if __name__ == '__main__':
    main()
