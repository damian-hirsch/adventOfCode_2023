# Get data from .txt file
def get_input() -> list:
    with open('input/Day02.txt', 'r') as file:
        # Remove space, split lines, and write each line to list
        data = file.read().splitlines()
    return data


# Solves part 1
def part_one(data: list) -> int:
    # Initialize total for end result
    total = 0
    # Check all games
    for i, game in enumerate(data):
        # Clean the string, remove Games
        game = game.strip().split(': ')[1].split('; ')
        # Check each sub game
        for sub_game in game:
            # Initialize results
            results = {'red': 0, 'green': 0, 'blue': 0}
            # Check each ball drawn
            for balls in sub_game.split(', '):
                # There is always a number and a color
                number, color = balls.split()
                # Set that color to the number of balls
                results[color] = int(number)
            # Check if game is impossible
            if results['red'] > 12 or results['green'] > 13 or results['blue'] > 14:
                break
        # If we don't break, we know the game was possible, add the game ID (which is index + 1)
        else:
            total += i + 1
    return total


# Solves part 2
def part_two(data: list) -> int:
    # Initialize total for end result
    total = 0
    # Check all games
    for i, game in enumerate(data):
        # Clean the string
        game = game.strip().split(': ')[1].split('; ')
        # Initialize results
        results = {'red': 0, 'green': 0, 'blue': 0}
        # Check each sub game
        for sub_game in game:
            # Check each ball drawn
            for balls in sub_game.split(', '):
                # There is always a number and a color
                number, color = balls.split()
                # Check if the number is larger than the current one in the game
                if int(number) > results[color]:
                    # Replace with new highest number
                    results[color] = int(number)
        # For each game, calculate the power
        power = results['red'] * results['green'] * results['blue']
        # Sum up all powers
        total += power
    return total


def main():

    print('The sum of IDs is:', part_one(get_input()))
    print('The sum of power is:', part_two(get_input()))


if __name__ == '__main__':
    main()
