# Get data from .txt file
def get_input() -> list:
    with open('input/Day04.txt', 'r') as file:
        # Remove space, split lines, and write each line to list
        data = file.read().splitlines()
        # Initialize counts to store matches
        counts = []
        for line in data:
            # Remove the Game part
            line = line.split(': ')[1]
            # Split the winning and my numbers
            winning, mine = line.split(' | ')
            # Split the numbers from each and convert to sets
            winning = set(map(int, winning.split()))
            mine = set(map(int, mine.split()))
            # Find the intersection of these sets
            intersection = mine.intersection(winning)
            # Count the number of elements in the intersection and append to counts list
            counts.append(len(intersection))
    return counts


# Solves part 1
def part_one(counts: list) -> int:
    # Initialize points
    points = 0
    for count in counts:
        # Calculate points, make use of int to handle the 0-case (** -0.5 will be rounded to zero)
        points += int(2 ** (count - 1))
    return points


# Solves part 2
def part_two(counts: list) -> int:
    # Initially we have one of each card
    num_cards = [1] * len(counts)
    for i, count in enumerate(counts):
        # Update scratch cards number by adding 1 to the number of following cards
        for j in range(1, count + 1):
            # Check to avoid index out of range error
            if i + j < len(counts):
                num_cards[i + j] += num_cards[i]
    return sum(num_cards)


def main():

    print('The total points is:', part_one(get_input()))
    print('The total scratchcards is:', part_two(get_input()))


if __name__ == '__main__':
    main()
