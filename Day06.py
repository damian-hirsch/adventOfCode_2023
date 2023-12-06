# Get data from .txt file
def get_input() -> tuple[list, list]:
    with open('input/Day06.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # First line: take right part of :, strip all whitespace around, split at whitespace and map to integers
        times = list(map(int, data[0].split(':')[1].strip().split()))
        # Second line: take right part of :, strip all whitespace around, split at whitespace and map to integers
        records = list(map(int, data[1].split(':')[1].strip().split()))
    return times, records


# Formula to calculate the distance, where x is the hold time and t_tot is the available time
def formula(x: int, t_tot: int) -> int:
    return x * (t_tot - x)


# Solves part 1
def part_one(data: tuple[list, list]) -> int:
    times, records = data
    result = 1
    # Go through each race
    for i, time in enumerate(times):
        distances = []
        # Create a list of distances
        for t in range(0, time):
            distances.append(formula(t, time))
        # Check each distance against the record and get the count of distances that beat the record back
        count = len([x for x in distances if x > records[i]])
        # Multiply these counts together
        result *= count
    return result


# Solves part 2
def part_two(data: tuple[list, list]) -> int:
    times, records = data
    # Merge the integers in the lists into one integer number
    time = int(''.join(str(i) for i in times))
    record = int(''.join(str(i) for i in records))
    # Note: The function that gets the distance is a symmetric (along y), negative parabolic function, this means that
    # once we have the time with a distance that beats the record, we know all other "timings" until the symmetric value
    # on the "other side" will beat the record.
    # Initialize t for PEP
    t = None
    for t in range(0, time):
        # Calculate distance
        distance = formula(t, time)
        # Check if distance beats record
        if distance > record:
            # We found the smallest time that beats the record
            break
    # Use symmetry to calculate the number of possible ways
    return time - 2 * t + 1


def main():

    print('Multiplying these numbers gets:', part_one(get_input()))
    print('This many ways can beat the record in the much longer race:', part_two(get_input()))


if __name__ == '__main__':
    main()
