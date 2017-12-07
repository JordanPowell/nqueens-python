# Row by row dfs and bfs candidates to the n-queens problem

# This is written to be easy to read and understand, is very slow and
# doesn't make proper use of the classes/functions/libraries that a
# real-world program should

# If you have any comments or questions, hit me up through github


N = 8
rows = N
cols = N


NO_SOLUTION = None

def dfs_iterative():
    initial_candidate = make_initial_candidate(col=0)

    open_list = [initial_candidate]
    while open_list:
        current_candidate = open_list.pop(0)
        any_queens_attacking_each_other = get_any_queens_attacking_each_other(current_candidate)
        if not any_queens_attacking_each_other:
            if board_is_full_of_queens(current_candidate):
                return current_candidate
            else:
                # Pushing candidates to the front makes this depth first
                open_list = get_next_candidates(current_candidate) + open_list
    return NO_SOLUTION


def dfs_recursive():
    def recurse(candidate):
        any_queens_attacking_each_other = get_any_queens_attacking_each_other(candidate)
        if any_queens_attacking_each_other:
            return NO_SOLUTION
        else:
            if board_is_full_of_queens(candidate):
                return candidate
            else:
                for next_candidate in get_next_candidates(candidate):
                    result = recurse(next_candidate)
                    if result != NO_SOLUTION:
                        return result
    return recurse(make_initial_candidate(col=0))


def bfs_iterative():
    initial_candidate = make_initial_candidate(col=0)

    open_list = [initial_candidate]
    while open_list:
        current_candidate = open_list.pop(0)
        any_queens_attacking_each_other = get_any_queens_attacking_each_other(current_candidate)
        if not any_queens_attacking_each_other:
            if board_is_full_of_queens(current_candidate):
                return current_candidate
            else:
                # Pushing candidates to the back makes this breadth first
                open_list = open_list + get_next_candidates(current_candidate)
    return NO_SOLUTION

# No BFS recursive because that's silly





# Candidate solutions are lists of columns - one queen per row at the column
def make_candidate(col=0, base_candidate=None):
    if base_candidate:
        return base_candidate[:] + [col]
    else:
        return [col]


def get_num_rows_in_candidate(candidate):
    return len(candidate)


def get_row(candidate, row=0):
    if row < get_num_rows_in_candidate(candidate):
        return candidate[row]
    return None


def get_queen_position_in_row(row):
    return row


def print_candidate(candidate):
    if candidate == NO_SOLUTION:
        print('No solution')
    else:
        for row in range(rows):
            queen_position = get_queen_position_in_row(get_row(candidate, row))
            for col in range(cols):
                if col == queen_position:
                    print(' Q ', end='')
                else:
                    print(' - ', end='')
            print()
            

def make_initial_candidate(col):
    return make_candidate(col)


def position_in_range(position):
    row, col = position
    return row < rows and row >= 0 and col < cols and col >= 0


def num_queens_in_positions(candidate, positions):
    num_queens = 0
    for pos_row, pos_col in positions:
        for cand_row, cand_col in enumerate(candidate):
            if pos_row == cand_row and pos_col == cand_col:
                num_queens = num_queens + 1
    return num_queens


def num_queens_in_row(candidate, row):
    positions = []
    for col in range(cols):
        positions.append((row, col))
    return num_queens_in_positions(candidate, positions)


def num_queens_in_column(candidate, col):
    positions = []
    for row in range(rows):
        positions.append((row, col))
    return num_queens_in_positions(candidate, positions)


def num_queens_on_diagonals(candidate, row, col):
    # This would be potentially better written recursively
    # or at least more intelligently
    # or just better at all
    positions = set()
    r = row
    c = col
    position = (r, c)
    while position_in_range(position):
        positions.add(position)
        r = r + 1
        c = c + 1
        position = (r, c)
    r = row
    c = col
    position = (r, c)
    while position_in_range(position):
        positions.add(position)
        r = r - 1
        c = c + 1
        position = (r, c)
    r = row
    c = col
    position = (r, c)
    while position_in_range(position):
        positions.add(position)
        r = r + 1
        c = c - 1
        position = (r, c)
    r = row
    c = col
    position = (r, c)
    while position_in_range(position):
        positions.add(position)
        r = r - 1
        c = c - 1
        position = (r, c)
    return num_queens_in_positions(candidate, positions)


def get_any_queens_attacking_each_other(candidate):
    for row, col in enumerate(candidate):
        # There's a queen at row, col
        if num_queens_in_row(candidate, row) > 1:
            return True
        if num_queens_in_column(candidate, col) > 1:
            return True
        if num_queens_on_diagonals(candidate, row, col) > 1:
            return True
    return False


def board_is_full_of_queens(candidate):
    return get_num_rows_in_candidate(candidate) == rows


def get_next_candidates(base_candidate):
    next_candidates = []
    for col in range(cols):
        next_candidates.append(make_candidate(col, base_candidate=base_candidate))
    return next_candidates


def main():
    candidate = dfs_iterative()
    print_candidate(candidate)


if __name__ == "__main__":
    main()


# Written drunkenly one evening after my dog died - don't judge too harshly
