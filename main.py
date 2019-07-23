import sys
import copy
import random


class Game:
    def __init__(self):
        """
        Initiate 4x4 self.grid and 4x4 self.merge_map with all zeros.
        """
        self.grid = [[0] * 4 for _ in range(4)]
        self.merge_map = [[0] * 4 for _ in range(4)]

    def initialize(self):
        """
        Initialize the game and randomly fill in 2 empty cells with 2 or 4.
        """
        empty_cells = self.empty_cells()
        success = self.fill_empty_cell(empty_cells, 2)
        if not success:
            raise Exception('Fill empty cell does not work normally!')

    def reset_merge_map(self):
        """
        A helper function to reset self.merge_map
        """
        self.merge_map = [[0] * 4 for _ in range(4)]

    def print_grid(self):
        """
        A helper function to print self.grid
        """
        for row in self.grid:
            print(row)
        print()

    def start(self):
        """
        Start function for human play
        """
        self.initialize()
        self.print_grid()
        while True:
            direction = input("Input your move (up, down, left, right): ")
            moved = self.move(direction)
            if not moved:
                print("{} is not a valid move!".format(direction))
            self.print_grid()
            game_over, msg = self.is_game_over()
            if game_over:
                print(msg)
                sys.exit(0)

    def empty_cells(self):
        """
        Find indexes of all empty cells in a grid.

        Returns:
            A list of tuples of indexes of empty cells
        """
        empty_cells = []
        for row in range(4):
            for column in range(4):
                if not self.grid[row][column]:
                    empty_cells.append((row, column))
        return empty_cells

    def fill_empty_cell(self, empty_cells, n=1):
        """
        Randomly fill in n empty cells of the grid with 2 or 4.

        Returns:
            True if success, False if not
        """
        while n > 0:
            if empty_cells:
                n -= 1
                index = random.randrange(len(empty_cells))
                row, column = empty_cells[index]
                del empty_cells[index]
                self.grid[row][column] = random.choice([2, 4])
            else:
                return False
        return True

    def is_game_over(self):
        """
        Check if game is over or not.

        Returns:
            True with win msg if 2048 is found.
            True with lose msg if no possible moves.
            False with no msg if game if possible moves exist.
        """
        for row in range(4):
            for column in range(4):
                if self.grid[row][column] == 2048:
                    return True, "Game finishes, you win!"

        possible_move = self.valid_move_exists()
        if possible_move:
            return False, ""
        else:
            return True, "Game over, no possible move, you lost!"

    def valid_move_exists(self):
        """
        Copy the grid into a deep copy and check if valid moves exist.

        Returns:
            True if valid moves exist, False otherwise.
        """
        grid_copy = copy.deepcopy(self.grid)
        copy_game = Game()
        copy_game.grid = grid_copy

        moved = copy_game.up()
        if moved:
            return True
        moved = copy_game.down()
        if moved:
            return True
        moved = copy_game.left()
        if moved:
            return True
        moved = copy_game.right()
        if moved:
            return True
        return False

    def can_move(self, row_1, col_1, row_2, col_2):
        """
        Check if the cell move from [row_1, col_1] to [row_2, col_2].

        Args:
            row_1: Row number of source
            col_1: Column number of source
            row_2: Row number of destination
            col_2: Column number of destination

        Returns:
            True if move is possible, False otherwise.
        """
        if self.grid[row_1][col_1] == 0:
            # Empty cells cannot move
            return False
        if self.merge_map[row_1][col_1]:
            # Merged cell cannot move twice in same round
            return False
        elif self.grid[row_1][col_1] == self.grid[row_2][col_2]\
                and self.merge_map[row_2][col_2] != 1:
            # Merge cell happens only when no merge happened in dest location
            return True
        elif not self.grid[row_2][col_2]:
            # Destination is an empty cell
            return True
        else:
            return False

    def move_cell(self, row_1, col_1, row_2, col_2):
        """
        Move the cell from [row_1, col_1] to [row_2, col_2]
        Set self.merge_map[row_2][col_2] to 1 if the move incurs a merge.

        Args:
            row_1: Row number of source
            col_1: Column number of source
            row_2: Row number of destination
            col_2: Column number of destination

        Returns:
            True if move happened, False otherwise.
        """
        if not self.grid[row_2][col_2]:
            # Destination is an empty cell
            self.grid[row_2][col_2] = self.grid[row_1][col_1]
            self.grid[row_1][col_1] = 0
        elif self.grid[row_1][col_1] == self.grid[row_2][col_2]:
            # Merge cell
            self.grid[row_2][col_2] += self.grid[row_1][col_1]
            self.grid[row_1][col_1] = 0
            self.merge_map[row_2][col_2] = 1
        else:
            return False
        return True

    def up(self):
        """
        Move all cells in row[1], row[2], row[3] upwards.
        Reset self.merge_map before return

        Returns:
            True if move happened, False otherwise.
        """
        moved = False
        for row in range(1, 4):
            for col in range(4):
                current_row = row
                while (current_row > 0 and
                       self.can_move(current_row, col,
                                     current_row-1, col)):
                    moved = self.move_cell(current_row, col,
                                           current_row-1, col)
                    current_row -= 1
        self.reset_merge_map()
        return moved

    def down(self):
        """
        Move all cells in row[0], row[1], row[2] downwards.
        Reset self.merge_map before return

        Returns:
            True if move happened, False otherwise.
        """
        moved = False
        for row in reversed(range(0, 3)):
            for col in range(4):
                current_row = row
                while (current_row < 3 and
                       self.can_move(current_row, col,
                                     current_row+1, col)):
                    moved = self.move_cell(current_row, col,
                                           current_row+1, col)
                    current_row += 1
        self.reset_merge_map()
        return moved

    def left(self):
        """
        Move all cells in col[1], col[2], col[3] leftwards.
        Reset self.merge_map before return

        Returns:
            True if move happened, False otherwise.
        """
        moved = False
        for col in range(1, 4):
            for row in range(4):
                current_col = col
                while (current_col > 0 and
                       self.can_move(row, current_col,
                                     row, current_col-1)):
                    moved = self.move_cell(row, current_col,
                                           row, current_col-1)
                    current_col -= 1
        self.reset_merge_map()
        return moved

    def right(self):
        """
        Move all cells in col[0], col[1], col[2] rightwards.
        Reset self.merge_map before return

        Returns:
            True if move happened, False otherwise.
        """
        moved = False
        for col in reversed(range(0, 3)):
            for row in range(4):
                current_col = col
                while (current_col < 3 and
                       self.can_move(row, current_col,
                                     row, current_col+1)):
                    moved = self.move_cell(row, current_col,
                                           row, current_col+1)
                    current_col += 1
        self.reset_merge_map()
        return moved

    def move(self, direction):
        """
        Move the grid into direction which player inputs.
        If the move is possible, move the grid and fill in an empty cell
        with 2 or 4, returns True.
        If the move is not possible, return False.

        Args:
            direction: Direction which player inputs

        Returns:
            True if the move happened, false otherwise.
        """
        moved = False
        if direction == "up":
            moved = self.up()
        elif direction == "down":
            moved = self.down()
        elif direction == "left":
            moved = self.left()
        elif direction == "right":
            moved = self.right()
        if moved:
            empty_cells = self.empty_cells()
            success = self.fill_empty_cell(empty_cells)
            if not success:
                raise Exception('Fill empty cell does not work normally!')
        return moved

    def bot_start(self):
        """
        Start function for my AI algorithm
        Move preference: down > left > right > up
        Immediately perform down if up is inevitably performed
        """
        self.initialize()
        self.print_grid()
        step_count = 0
        while True:
            moved = self.move('down')
            direction = 'down'
            is_up = False
            if not moved:
                print("{} is not a valid move!".format(direction))
                self.print_grid()
                moved = self.move('left')
                direction = 'left'
                if not moved:
                    print("{} is not a valid move!".format(direction))
                    self.print_grid()
                    moved = self.move('right')
                    direction = 'right'
                    if not moved:
                        print("{} is not a valid move!".format(direction))
                        self.print_grid()
                        moved = self.move('up')
                        direction = 'up'
                        if moved:
                            is_up = True
                        else:
                            print("{} is not a valid move!".format(direction))
                            self.print_grid()

            if moved:
                step_count += 1
                print("Step {}, {}".format(step_count, direction))

            if is_up:
                self.move('down')
                step_count += 1
                print("Step {}, {}".format(step_count, 'down'))

            self.print_grid()
            game_over, msg = self.is_game_over()
            if game_over:
                print(msg)
                sys.exit(0)


def main():
    game = Game()
    game.bot_start()
    # game.start() for human


if __name__ == "__main__":
    main()
