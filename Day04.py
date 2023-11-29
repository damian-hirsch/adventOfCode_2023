# Get data from .txt file
def get_input() -> list:
    with open('input/Day04.txt', 'r') as file:
        # Remove space, split lines, and write each line to list
        data = file.read().replace(' ', '').splitlines()
    return data


# Solves part 1
def part_one(data: list) -> int:
    return 1


# Solves part 2
def part_two(data: list) -> int:
    return 1


def main():

    print('The score would be:', part_one(get_input()))
    print('The score would be:', part_two(get_input()))


if __name__ == '__main__':
    main()
