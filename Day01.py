import re


# Get data from .txt file
def get_input() -> list:
    with open('input/Day01.txt', 'r') as file:
        # Split lines, and write each line to list
        data = file.read().splitlines()
    return data


# Solves part 1
def part_one(data: list[str]) -> int:
    # Initialize values list
    values = []
    # In regex we are looking for digits
    pattern = r'\d'
    for line in data:
        # Find the first digit
        first_digit = re.search(pattern, line).group()
        # Find the last digit by reverting the string
        last_digit = re.search(pattern, line[::-1]).group()
        # Combine both strings, convert to integer, and append to values list
        values.append(int(first_digit + last_digit))
    # Sum all numbers in values list
    return sum(values)


# Solves part 2
def part_two(data: list[str]) -> int:
    # Create dictionary to map different results, for simplicity (avoiding if or try catch clauses) also the numbers
    num_dict = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }
    # Initialize values list
    values = []
    # Now we are looking for all digits or the written out numbers, we allow overlap (positive lookahead)
    pattern_first = r'(?=(\d|zero|one|two|three|four|five|six|seven|eight|nine))'
    for line in data:
        # Find all digits
        digits = re.findall(pattern_first, line)
        # We take the first and last digit in the list and convert the string numbers using the dictionary. Note because
        # we don't merge, the first digit needs to be multiplied by 10
        values.append(num_dict[digits[0]] * 10 + num_dict[digits[-1]])
    # Sum all numbers in values list
    return sum(values)


def main():

    print('The sum of all calibration values is:', part_one(get_input()))
    print('the sum of all calibration values is:', part_two(get_input()))


if __name__ == '__main__':
    main()
