assignments = []


# OK
def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]


all_digits = '123456789'
rows = 'ABCDEFGHI'
cols = all_digits
cols_reversal = all_digits[::-1]
boxes = cross(rows, cols)

horizontal_units = [cross(rows, c) for c in cols]
vertical_units = [cross(r, cols) for r in rows]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[rows[i]+cols[i] for i in range(len(rows))]] + [[rows[i]+cols_reversal[i] for i in range(len(rows))]]

unit_list = horizontal_units + vertical_units + square_units + diagonal_units

units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # First select boxes with 2 entries
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    # Collect boxes that have the same elements
    naked_twins = [[box1, box2] for box1 in potential_twins for box2 in peers[box1] if set(values[box1]) == set(values[box2])]

    # For each pair of naked twins,
    for i in range(len(naked_twins)):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        # 1- compute intersection of peers
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_int = peers1 & peers2
        # 2- Delete the two digits in naked twins from all common peers.
        for peer_val in peers_int:
            if len(values[peer_val]) > 1:
                inner = values[box1]
                for rm_val in inner:
                    values = assign_value(values, peer_val, values[peer_val].replace(rm_val, ''))
    return values

# OK
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = [c for c in grid if c in all_digits or c in '0.']
    for index, item in enumerate(chars):
        if item in '0.':
            chars[index] = '123456789'
    assert len(chars) == 81
    return dict(zip(boxes, chars))


# OK
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)

    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    return


# OK
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]

        for peer in peers[box]:
            # values[peer] = values[peer].replace(digit, '')
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


# OK
def only_choice(values):
    for unit in unit_list:
        for digit in all_digits:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


# OK
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


# OK
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled boxes with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


for_test = {"G7": "2345678", "G6": "1236789", "G5": "23456789", "G4": "345678", "G3": "1234569", "G2": "12345678", "G1": "23456789", "G9": "24578", "G8": "345678", "C9": "124578", "C8": "3456789", "C3": "1234569", "C2": "1234568", "C1": "2345689", "C7": "2345678", "C6": "236789", "C5": "23456789", "C4": "345678", "E5": "678", "E4": "2", "F1": "1", "F2": "24", "F3": "24", "F4": "9", "F5": "37", "F6": "37", "F7": "58", "F8": "58", "F9": "6", "B4": "345678", "B5": "23456789", "B6": "236789", "B7": "2345678", "B1": "2345689", "B2": "1234568", "B3": "1234569", "B8": "3456789", "B9": "124578", "I9": "9", "I8": "345678", "I1": "2345678", "I3": "23456", "I2": "2345678", "I5": "2345678", "I4": "345678", "I7": "1", "I6": "23678", "A1": "2345689", "A3": "7", "A2": "234568", "E9": "3", "A4": "34568", "A7": "234568", "A6": "23689", "A9": "2458", "A8": "345689", "E7": "9", "E6": "4", "E1": "567", "E3": "56", "E2": "567", "E8": "1", "A5": "1", "H8": "345678", "H9": "24578", "H2": "12345678", "H3": "1234569", "H1": "23456789", "H6": "1236789", "H7": "2345678", "H4": "345678", "H5": "23456789", "D8": "2", "D9": "47", "D6": "5", "D7": "47", "D4": "1", "D5": "36", "D2": "9", "D3": "8", "D1": "36"}
display(for_test)
res = naked_twins(for_test)
print('\n')
display(res)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # display(solve(diag_sudoku_grid))
    display(search(for_test))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
