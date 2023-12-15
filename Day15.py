# Get data from .txt file
def get_input() -> list:
    with open('input/Day15.txt', 'r') as file:
        # Split line and create list
        data = list(file.read().split(','))
    return data


# Hash algorithm
def hash_alg(string: str) -> int:
    value = 0
    # Go through each char of the string
    for char in string:
        # Calculate value
        value = (value + ord(char)) * 17 % 256
    return value


# Solves part 1
def part_one(data: list) -> int:
    values = []
    # Go through initialization sequence
    for entry in data:
        # Calculate hash and append value
        values.append(hash_alg(entry))
    return sum(values)


# Solves part 2
def part_two(data: list) -> int:
    # Initialize boxes
    boxes = [[] for _ in range(256)]
    # Go through initialization sequence
    for entry in data:
        # Check if we have a removal
        if entry[-1] == '-':
            # Get the label
            label = entry[:-1]
            # Get the current box at the hash of this label
            box = boxes[hash_alg(label)]
            # Initialized new box
            new_box = []
            # Go through all lenses already in this box
            for lens in box:
                # If the label doesn't match the label on the lens, add it back (otherwise it will be removed = not
                # added back)
                if label != lens[0]:
                    new_box.append((lens[0], lens[1]))
            # Update the box
            boxes[hash_alg(label)] = new_box
        # Else we have a lens addition
        else:
            # Get the focal length
            num = int(entry[-1])
            # Get the label
            label = entry[:-2]
            # Get the current box at the hash of this label
            box = boxes[hash_alg(label)]
            # Initialized new box
            new_box = []
            # Initialized value to see if we replaced a lens with a different focal length
            was_replaced = False
            # Go through each lens in the box
            for lens in box:
                # If we don't have the same lens, keep it in the box
                if label != lens[0]:
                    new_box.append((lens[0], lens[1]))
                # Else, replace it with the new focal length
                else:
                    was_replaced = True
                    new_box.append((lens[0], num))
            # At the end of the for loop
            else:
                # If the new lens was not a replacement, add it to the box as well
                if not was_replaced:
                    new_box.append((label, num))
            # Update the box
            boxes[hash_alg(label)] = new_box

    # Calculate focusing power
    total = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            total += (i + 1) * (j + 1) * lens[1]

    return total


def main():

    print('The sum of the results is:', part_one(get_input()))
    print('The focusing power of the resulting lens configuration is:', part_two(get_input()))


if __name__ == '__main__':
    main()
