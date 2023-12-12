import itertools
from functools import cache


# Get data from .txt file
def get_input() -> tuple[list, list]:
    with open('input/Day12.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Initialize lists
        records = []
        checks = []
        # Create records and checks lists
        for line in data:
            record, check = line.split()
            records.append(record)
            checks.append(list(map(int, check.split(','))))
    return records, checks


def replace_question_marks(base_string, replacements, positions):
    # Convert the string to a list for easy modification
    string_list = list(base_string)

    # Replace the question marks at the specified positions
    for pos, replacement in zip(positions, replacements):
        string_list[pos] = replacement

    return ''.join(string_list)


@cache  # Cache to significantly accelerate the computing time
def count_arg(sub_record, checks, check_counter=None):
    # If we finished all checks, and we also don't have a current one running, we have a valid arrangement if there is
    # no further '#'
    if len(checks) == 0 and check_counter is None:
        return '#' not in sub_record

    # We are using the slicing operation [:1] to avoid getting an index error when the string is empty if we try to
    # directly access it with sub_record[0]
    match sub_record[:1], check_counter:
        # If we have an empty string, and there is no check counter, or it's at 0, we have a valid arrangement if there
        # are no checks left, otherwise it's invalid
        case '', None | 0:
            return len(checks) == 0
        # If we have an empty string, and the check counter is not none or 0, we have an invalid arrangement
        case '', _:
            return 0

        # If the next char is a '?', and no check has been started, we need to split into two cases: '.' and '#'
        # If we assume a '.', we just move to the next character
        # If we assume a '#', we are now starting a contagious group of springs and need to start our check counter
        case '?', None:
            return count_arg(sub_record[1:], checks) + count_arg(sub_record, checks[1:], check_counter=checks[0])
        # If the next char is a '?', and the current check counter is at 0, we can only have a '.', because the '#' case
        # would be an invalid arrangement
        case '?', 0:
            return count_arg(sub_record[1:], checks)
        # If the next char is a '?', and the current check counter is not 0, we can only have a '#', we reduce the check
        # counter by 1. The '.' case would be an invalid arrangement.
        case '?', _:
            return count_arg(sub_record[1:], checks, check_counter=check_counter-1)

        # If the next char is a '#', and we currently have no check counter running, we start it
        case '#', None:
            return count_arg(sub_record, checks[1:], check_counter=checks[0])
        # If the next char is a '#', and the check counter is at 0, we have an invalid arrangement
        case '#', 0:
            return 0
        # If the next char is a '#', and the check counter is not none or 0, we reduce the check counter by 1
        case '#', _:
            return count_arg(sub_record[1:], checks, check_counter=check_counter-1)

        # If the next char is a '.', and there is no check counter, or it's at 0, we move to the next char
        case '.', None | 0:
            return count_arg(sub_record[1:], checks)
        # If the next char is a '.', and the check counter is not none or 0, we have an invalid arrangement
        case '.', _:
            return 0


# Solves part 1 (old)
# Note, this is the brute force approach and takes a few seconds to calculate (this will not work for part 2)
def part_one_old(records: list, checks: list) -> int:
    count = 0
    for i, record in enumerate(records):
        # Find positions of the question marks
        positions = [i for i, c in enumerate(record) if c == '?']

        # Generate all combinations of '.' and '#' for the question marks
        combinations = itertools.product('.#', repeat=len(positions))

        # Replacing the question marks with each combination
        all_combinations = [replace_question_marks(record, combo, positions) for combo in combinations]

        # Check each combination for validity
        for combination in all_combinations:
            # Split the string using '.' as the delimiter, remove empty entries, and calculate the length of each #
            # group to get the same style of list as the arrangements
            candidate = [len(s) for s in combination.split('.') if s]
            # Compare the list to the actual check and see if it is valid
            if candidate == checks[i]:
                count += 1
    return count


# Solves part 1
def part_one(records: list, checks: list) -> int:
    count = 0
    for i, record in enumerate(records):
        # Get the check and convert to tuple for hashing
        check = tuple(checks[i])

        # Calculate total arrangements
        count += count_arg(record, check)
    return count


# Solves part 2
def part_two(records: list, checks: list) -> int:
    count = 0
    for i, record in enumerate(records):
        # Expand the record five times separated by ?
        record = '?'.join([record] * 5)
        # Expand the check 5 times and convert to a tuple for hashing
        check = tuple(checks[i] * 5)

        # Calculate total arrangements
        count += count_arg(record, check)
    return count


def main():

    print('The sum of those counts is:', part_one(*get_input()))
    print('The new sum of possible arrangement counts is:', part_two(*get_input()))


if __name__ == '__main__':
    main()
