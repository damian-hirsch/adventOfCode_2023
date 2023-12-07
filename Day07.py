# Get data from .txt file
def get_input() -> list[tuple[str, int]]:
    with open('input/Day07.txt', 'r') as file:
        # Splitlines
        data = file.read().splitlines()
        hands = []
        # For each line, split it and append to hands list
        for line in data:
            hand, bid = line.split()
            hands.append((hand, int(bid)))
    return hands


def classify_poker_hand_p1(hand) -> int:
    # Five of a kind
    if len(set(hand)) == 1:
        return 7
    elif len(set(hand)) == 2:
        counts = [hand.count(card) for card in set(hand)]
        # Four of a kind
        if 4 in counts:
            return 6
        # Full house
        elif 3 in counts and 2 in counts:
            return 5
    elif len(set(hand)) == 3:
        counts = [hand.count(card) for card in set(hand)]
        # Three of a kind
        if 3 in counts:
            return 4
        # Two pairs
        elif counts.count(2) == 2:
            return 3
    # Pairs
    elif len(set(hand)) == 4:
        return 2
    # High card
    else:
        return 1


def classify_poker_hand_p2(hand) -> int:
    # Count the number of jokers
    count_j = hand.count('J')
    # Five of a kind
    if len(set(hand)) == 1:
        return 7
    elif len(set(hand)) == 2:
        counts = [hand.count(card) for card in set(hand)]
        # Four of a kind
        if 4 in counts:
            # If there are any jokers, we can make five of a kind
            if count_j in (1, 4):
                return 7
            else:
                return 6
        # Full house
        elif 3 in counts and 2 in counts:
            # If there are any jokers, we can make five of a kind
            if count_j in (2, 3):
                return 7
            else:
                return 5
    elif len(set(hand)) == 3:
        counts = [hand.count(card) for card in set(hand)]
        # Three of a kind
        if 3 in counts:
            # If there are jokers, we can make four of a kind
            if count_j in (1, 3):
                return 6
            else:
                return 4
        # Two pairs
        elif counts.count(2) == 2:
            # If any of the pairs are jokers, we can make four of a kind
            if count_j == 2:
                return 6
            # If the single card is a joker, we can make a full house
            elif count_j == 1:
                return 5
            else:
                return 3
    # Pair
    elif len(set(hand)) == 4:
        # If there are any jokers, we can make three of a kind
        if count_j in (1, 2):
            return 4
        else:
            return 2
    # High card
    else:
        # If there is a joker, we can make a pair
        if count_j == 1:
            return 2
        return 1


def hand_value_p1(cards: str) -> tuple[int, tuple]:
    # Get card classification (five of a kind, four of a kind, etc.)
    classification = classify_poker_hand_p1(cards)
    # Definition of order (low to high)
    order = '23456789TJQKA'
    # Give each character a value
    rank_values = {rank: index for index, rank in enumerate(order)}
    # Evaluate the cards
    card_value = tuple(rank_values[card] for card in cards)
    # Return classification and card value
    return classification, card_value


def hand_value_p2(cards: str) -> tuple[int, tuple]:
    # Get card classification (five of a kind, four of a kind, etc.)
    classification = classify_poker_hand_p2(cards)
    # Definition of order (low to high)
    order = 'J23456789TQKA'
    # Give each character a value
    rank_values = {rank: index for index, rank in enumerate(order)}
    # Evaluate the cards
    card_value = tuple(rank_values[card] for card in cards)
    # Return classification and card value
    return classification, card_value


# Solves part 1
def part_one(hands: list) -> int:
    # Sort hands based on classification and card value
    hands.sort(key=lambda hand: hand_value_p1(hand[0]))
    # Create multiplier
    multiplier = list(range(1, len(hands) + 1))
    # Get bids
    hand_bids = [hand[1] for hand in hands]
    # Multiply corresponding elements and sum them
    winnings = sum(a * b for a, b in zip(hand_bids, multiplier))
    return winnings


# Solves part 2
def part_two(hands: list) -> int:
    # Sort hands based on classification and card value
    hands.sort(key=lambda hand: hand_value_p2(hand[0]))
    # Create multiplier
    multiplier = list(range(1, len(hands) + 1))
    # Get bids
    hand_bids = [hand[1] for hand in hands]
    # Multiply corresponding elements and sum them
    winnings = sum(a * b for a, b in zip(hand_bids, multiplier))
    return winnings


def main():
    print('The total winnings are:', part_one(get_input()))
    print('The new total winnings are:', part_two(get_input()))


if __name__ == '__main__':
    main()
