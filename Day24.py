import numpy as np
from sympy import symbols, solve


# Get data from .txt file
def get_input() -> tuple[np.ndarray, np.ndarray]:
    with open('input/Day24.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        pos = []
        vel = []
        for line in data:
            po, ve = line.split('@')
            pos.append(list(map(int, po.split(','))))
            vel.append(list(map(int, ve.split(','))))
        # Convert lists to np arrays
        pos_array = np.array(pos)
        vel_array = np.array(vel)
    return pos_array, vel_array


def check_intersection(x1: np.ndarray, x2: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> tuple:
    # Setting up the system of equations
    a = np.column_stack((v1, -v2))
    b = np.array(x2 - x1)

    # Solve equation A*x + b = 0
    t = np.linalg.solve(a, b)

    # The point of intersection
    ip = (x1[0] + t[0] * v1[0], x1[1] + t[0] * v1[1])

    return ip, t


# Solves part 1
def part_one(pos: np.ndarray, vel: np.ndarray) -> int:
    lower_bound, upper_bound = 200000000000000, 400000000000000
    count = 0
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            # Check for parallelity
            if np.all(np.cross(vel[i][:2], vel[j][:2]) == 0):
                continue
            else:
                # Calculate
                ip, t = check_intersection(pos[i][:2], pos[j][:2], vel[i][:2], vel[j][:2])
                # Check if we have values in the future
                if np.all(t > 0) and lower_bound <= ip[0] <= upper_bound and lower_bound <= ip[1] <= upper_bound:
                    count += 1
    return count


# Solves part 2
def part_two(pos: list, vel: list) -> int:
    x, y, z, vx, vy, vz = symbols('x y z vx vy vz', integer=True)

    equations = []
    answers = []
    for i in range(len(pos)):
        # We can also check for collision using the cross product of the relative position with the relative velocity.
        # If that equals 0, then we know that they are either parallel or anti-parallel. Combined with the dot product,
        # if they are anti-parallel (dot product is negative), a collision is possible.
        equations.append((y - pos[i][1]) * (vz - vel[i][2]) - (z - pos[i][2]) * (vy - vel[i][1]))
        equations.append((z - pos[i][2]) * (vx - vel[i][0]) - (x - pos[i][0]) * (vz - vel[i][2]))
        equations.append((x - pos[i][0]) * (vy - vel[i][1]) - (y - pos[i][1]) * (vx - vel[i][0]))

        # We need at least 6 equations to solve for 6 variables x, y, z, vx, vy, vz. Additional, we don't want to add an
        # inequality check for the dot product check, thus, we add another 3 to avoid any ambiguity.
        if i < 2:
            continue
        # Calculate an answer
        else:
            answers = solve(equations)
            # If we found a single answer, we are done. Else, for example if we have equivalent equations, which lead
            # multiple solutions, we continue to add more. This is unlikely though, because we already have 9 equations
            # to work with to solve for 6 variables and 1 direction.
            if len(answers) == 1:
                break

    answer = answers[0]
    return answer[x] + answer[y] + answer[z]


def main():

    print('This many of these intersections occur within the test area:', part_one(*get_input()))
    print('If you add up the X, Y, and Z coordinates of that initial position you get:', part_two(*get_input()))


if __name__ == '__main__':
    main()
