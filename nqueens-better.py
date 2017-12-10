# This is a bit better but still doesn't have error checking etc.
# It's also really really slow because it's not optimised
# If you have any comments or questions, hit me up through github


N = 8
rows = N
cols = N


def dfs():
    def recurse(candidate):
        if candidate_is_full_solution(candidate):
            return candidate
        if candidate_is_potential_solution(candidate):
            for child_candidate in candidate.children:
                solution = recurse(child_candidate)
                if solution != NO_SOLUTION:
                    return solution
        return NO_SOLUTION
    return recurse(make_initial_candidate(col=0))


def candidate_is_potential_solution(candidate):
    return candidate.num_conflicting_queens == 0


def candidate_is_full_solution(candidate):
    return candidate.num_queens == rows and candidate_is_potential_solution(candidate)


def make_initial_candidate(col):
    return CandidateSolution.create(queens=[col])


class NoSolution(object):
    def __str__(self):
        return "No solution"
NO_SOLUTION = NoSolution()


def is_valid_position(position):
    row, col = position
    return row >= 0 and row < rows and col >=0 and col < cols


def is_diagonal(position_a, position_b):
    a_row, a_col = position_a
    b_row, b_col = position_b
    return abs(a_row - b_row) == abs(a_col - b_col)


class CandidateSolution(object):
    def __init__(self, queens):
        self._num_conflicting_queens = None
        self.queens = queens

    def _calculate_row_positions(self, row, col):
        return [(i, col) for i in range(cols)]

    def _calculate_col_positions(self, row, col):
        return [(row, i) for i in range(rows)]

    def _calculate_diagonal_positions(self, row, col):
        positions = []
        position = (row, col)
        for i in range(rows):
            for j in range(cols):
                if is_diagonal(position, (i, j)) and is_valid_position(position):
                    positions.append((i, j))
        return positions

    def _num_queens_in_positions(self, positions):
        num_queens = 0
        for row, col in set(positions):
            for queen_row, queen_col in enumerate(self.queens):
                if row == queen_row and col == queen_col:
                    num_queens = num_queens + 1
        return num_queens

    def _calculate_conflicts_for_queen(self, row, col):
        return self._num_queens_in_positions(self._calculate_row_positions(row, col) + self._calculate_col_positions(row, col) + self._calculate_diagonal_positions(row, col)) - 1

    def _calculate_num_conflicting_queens(self):
        return sum([self._calculate_conflicts_for_queen(queen_row, queen_col) for queen_row, queen_col in enumerate(self.queens)])

    @property
    def num_queens(self):
        return len(self.queens)

    @property
    def num_conflicting_queens(self):
        if self._num_conflicting_queens is None:
            self._num_conflicting_queens = self._calculate_num_conflicting_queens()
        return self._num_conflicting_queens

    @property 
    def children(self):
        # Could cache this but it's only called once
        return [self._create_child(i) for i in range(cols)]

    def _create_child(self, col):
        return CandidateSolution.create(queens=self.queens + [col])

    @staticmethod
    def create(queens):
        return CandidateSolution(queens)

    def __str__(self):
        s = ''
        for row in range(rows):
            queen_position = -1 if row >= len(self.queens) else self.queens[row]
            for col in range(cols):
                if col == queen_position:
                    s = s +  ' Q '
                else:
                    s = s + ' - '
            s = s + '\n'
        return s


if __name__ == "__main__":
    dfs()
