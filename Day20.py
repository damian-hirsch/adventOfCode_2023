from collections import deque
from math import lcm


# Get data from .txt file
def get_input() -> dict:
    with open('input/Day20.txt', 'r') as file:
        # Split lines
        data = file.read().splitlines()
        # Module dictionary in the form {'name': (type, [connections], state)}
        module_dict = {}
        conjunction_list = []
        for line in data:
            type_name, connections = line.split(' -> ')
            module_type = type_name[0]
            module_name = type_name[1:]
            connections = connections.split(', ')
            # Broadcaster
            if module_type == 'b':
                module_dict[module_name] = ('b', connections, False)
            # Flip-flop
            elif module_type == '%':
                module_dict[module_name] = ('%', connections, False)
            # Conjunction
            elif module_type == '&':
                module_dict[module_name] = ('&', connections, {})
                conjunction_list.append(module_name)
            else:
                print('Unknown module type')
        # We need to go through the list a second time to build the receiver connections to the conjunction modules.
        # This cannot be done above, because we don't know at that point which conjunction models even exist
        for line in data:
            type_name, connections = line.split(' -> ')
            module_name = type_name[1:]
            connections = connections.split(', ')
            for connection in connections:
                if connection in conjunction_list:
                    module_dict[connection][2][module_name] = 0
    return module_dict


# Solves part 1
def part_one(module_dict: dict) -> int:
    # Initialize pulses
    low_pulses = 0
    high_pulses = 0
    # Go through 1000 button presses
    for i in range(1000):
        # Initialize signal of button press (low pulse)
        signals = deque([('roadcaster', 0, 'button')])
        # Button press sends a low pulse, add it
        low_pulses += 1
        # Work through all signals
        while signals:
            # Get signal properties
            target, signal, sender = signals.popleft()
            # Check if the target is even one of our modules, otherwise just continue (signal goes into void)
            if target in module_dict.keys():
                module_type, connections, state = module_dict[target]
            else:
                continue

            # Check the module type and perform respective action
            # Broadcaster
            if module_type == 'b':
                # Send same pulse to all of its connections
                for connection in connections:
                    signals.append((connection, state, target))
                    # Update pulse count accordingly
                    if state:
                        high_pulses += 1
                    else:
                        low_pulses += 1
            # Flip-flop
            elif module_type == '%':
                # If we have a low pulse
                if not signal:
                    for connection in connections:
                        # If on, send a low pulse
                        if state:
                            signals.append((connection, 0, target))
                            # Add low pulse
                            low_pulses += 1
                        # Else off, send a high pulse
                        else:
                            signals.append((connection, 1, target))
                            # Add high pulse
                            high_pulses += 1
                    # Switch on to off or off to on
                    module_dict[target] = (module_type, connections, not state)
            # Conjunction
            elif module_type == '&':
                # Update input state
                state[sender] = signal
                module_dict[target] = (module_type, connections, state)
                # Check if all prior inputs were high pulses, then send a low pulse
                if all(state.values()):
                    for connection in connections:
                        signals.append((connection, 0, target))
                        # Add low pulse
                        low_pulses += 1
                # Else, send a high pulse
                else:
                    for connection in connections:
                        signals.append((connection, 1, target))
                        # Add high pulse
                        high_pulses += 1
            else:
                print('Unknown module type')
    # Return total as the multiplication between the two pulse counts
    return high_pulses * low_pulses


# Solves part 2: Looking at my input, 'rx' is connected to a conjunction 'ls', but more interestingly that conjunction
# is connected to 4 different conjunctions. To make sure 'ls' output is a low pulse, its input needs to be all high
# pulses. We can thus check the cycles of high pulses for these 4 conjunctions and calculate the lcm.
def part_two(module_dict: dict) -> int:
    # Get modules that trigger 'rx' (will be 'ls') and get its states (which are its incoming connections in this case)
    trigger_modules = {}
    for key, value in module_dict.items():
        if 'rx' in value[1]:
            # Get the 4 trigger modules to 'ls', make sure we copy to avoid overwriting
            trigger_modules = module_dict[key][2].copy()
            break

    # Initialize counter and iteration limit as failsafe
    counter = 0
    max_iter = 10000000
    while counter < max_iter:
        # Check if we found all cycles for the trigger modules
        if all(value > 0 for value in trigger_modules.values()):
            return lcm(*list(trigger_modules.values()))

        # Button press: Send initial signal
        signals = deque([('roadcaster', 0, 'button')])
        # Increase counter of button press
        counter += 1
        # Work through all signals
        while signals:
            # Get signal properties
            target, signal, sender = signals.popleft()
            # Check if the target is even one of our modules, otherwise just continue (signal goes into void)
            if target in module_dict.keys():
                module_type, connections, state = module_dict[target]
            else:
                continue

            # Check the module type and perform respective action
            # Broadcaster
            if module_type == 'b':
                # Send same pulse to all of its connections
                for connection in connections:
                    signals.append((connection, state, target))
            # Flip-flop
            elif module_type == '%':
                # Only activates, if we have a low pulse
                if not signal:
                    for connection in connections:
                        # If on, send a low pulse
                        if state:
                            signals.append((connection, 0, target))
                        # Else off, send a high pulse
                        else:
                            signals.append((connection, 1, target))
                    # Switch on to off or off to on
                    module_dict[target] = (module_type, connections, not state)
            # Conjunction
            elif module_type == '&':
                # Update input state
                state[sender] = signal
                module_dict[target] = (module_type, connections, state)
                # Check if all prior inputs were high pulses, then send a low pulse
                if all(state.values()):
                    for connection in connections:
                        signals.append((connection, 0, target))
                # Else, send a high pulse
                else:
                    for connection in connections:
                        signals.append((connection, 1, target))
                        # Check if the target is one of our trigger modules, this is a high-pulse cycle
                        if target in trigger_modules.keys():
                            trigger_modules[target] = counter
            # It should never reach this
            else:
                print('Unknown module type')
    return -1


def main():

    print('The total number of low pulses multiplied by the total number of high pulses is:', part_one(get_input()))
    print("The fewest number of button presses for a low pulse to reach module 'rx' is:", part_two(get_input()))


if __name__ == '__main__':
    main()
