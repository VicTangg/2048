import pytest
from .main import Game


@pytest.fixture
def create_game():
    pass


def test_initialize():
    # Case 1 - New game has grid of all zeros
    game = Game()
    grid_sum = sum([sum(row) for row in game.grid])
    assert grid_sum == 0

    # Case 2 - New game after initialization have 2 cells with at least
    #          sum of 4
    for i in range(10000):
        game = Game()
        game.initialize()
        grid_sum = sum([sum(row) for row in game.grid])
        assert grid_sum > 3


def test_reset_merge_map():
    game = Game()

    # Case 1 - Merge map is not all zeros before reset runs
    game.merge_map[0][0] = 1
    assert game.merge_map != [[0] * 4 for _ in range(4)]

    # Case 2 - Merge map is all zeros after reset runs
    game.reset_merge_map()
    assert game.merge_map == [[0] * 4 for _ in range(4)]


def test_empty_cells():
    # Case 1 - 16 empty cells before game initialization
    game = Game()
    empty_cells_count = len(game.empty_cells())
    assert empty_cells_count == 16

    # Case 2 - 14 empty cells before after initialization
    for i in range(10000):
        game = Game()
        game.initialize()
        empty_cells_count = len(game.empty_cells())
        assert empty_cells_count == 14


def test_fill_empty_cells():
    # Case 1 - 16 empty cells before filling
    game = Game()
    empty_cells = game.empty_cells()
    assert len(empty_cells) == 16

    # Case 2 - 16 empty cells after filling 0
    game.fill_empty_cell(empty_cells, 0)
    empty_cells = game.empty_cells()
    assert len(empty_cells) == 16

    # Case 3 - 14 empty cells after filling 2
    game.fill_empty_cell(empty_cells, 2)
    empty_cells = game.empty_cells()
    assert len(empty_cells) == 14

    # Case 4 - 11 empty cells after further filling 3
    game.fill_empty_cell(empty_cells, 3)
    empty_cells = game.empty_cells()
    assert len(empty_cells) == 11


def test_is_game_over():
    game = Game()
    game.initialize()

    # Case 1 - Possible moves exist
    status, msg = game.is_game_over()
    assert status is False
    assert msg is ""

    # Case 2 - Game over with a loss
    game.grid[0][0] = 256
    game.grid[0][1] = 128
    game.grid[0][2] = 64
    game.grid[0][3] = 32
    game.grid[1][0] = 128
    game.grid[1][1] = 64
    game.grid[1][2] = 32
    game.grid[1][3] = 16
    game.grid[2][0] = 64
    game.grid[2][1] = 32
    game.grid[2][2] = 16
    game.grid[2][3] = 8
    game.grid[3][0] = 32
    game.grid[3][1] = 16
    game.grid[3][2] = 8
    game.grid[3][3] = 4
    status, msg = game.is_game_over()
    assert status is True
    assert msg == "Game over, no possible move, you lost!"

    # Case 3 - Game over with win
    game.grid[0][0] = 2048
    status, msg = game.is_game_over()
    assert status is True
    assert msg == "Game finishes, you win!"


def test_valid_move_exists():
    game = Game()
    # Case 1 - Valid moves exist
    game.initialize()
    assert game.valid_move_exists() is True

    # Case 2 - Valid moves do not exist
    game.grid[0][0] = 256
    game.grid[0][1] = 128
    game.grid[0][2] = 64
    game.grid[0][3] = 32
    game.grid[1][0] = 128
    game.grid[1][1] = 64
    game.grid[1][2] = 32
    game.grid[1][3] = 16
    game.grid[2][0] = 64
    game.grid[2][1] = 32
    game.grid[2][2] = 16
    game.grid[2][3] = 8
    game.grid[3][0] = 32
    game.grid[3][1] = 16
    game.grid[3][2] = 8
    game.grid[3][3] = 4
    assert game.valid_move_exists() is False


def test_can_move():
    game = Game()
    # Case 1 - Move is possible, empty destination
    game.grid[0][0] = 0
    game.grid[0][1] = 2
    assert game.can_move(0, 1, 0, 0) is True

    # Case 2 - Move is possible, merge at destination
    game.grid[0][0] = 2
    game.grid[0][1] = 2
    assert game.can_move(0, 1, 0, 0) is True

    # Case 3 - Move is not possible, source is zero
    game.grid[0][0] = 0
    game.grid[0][1] = 0
    assert game.can_move(0, 1, 0, 0) is False

    # Case 4 - Move is not possible, merge happened at destination
    game.grid[0][0] = 4
    game.grid[0][1] = 4
    game.merge_map[0][0] = 1
    assert game.can_move(0, 1, 0, 0) is False

    # Case 5 - Move is not possible, different values
    game.grid[0][0] = 2
    game.grid[0][0] = 4
    assert game.can_move(0, 1, 0, 0) is False


def test_move_cell():
    game = Game()
    # Case 1 - Move cell to empty destination
    game.grid[0][0] = 0
    game.grid[0][1] = 2
    game.move_cell(0, 1, 0, 0)
    assert game.grid[0][0] == 2
    assert game.grid[0][1] == 0

    # Case 2 - Merge cell at destination
    game.grid[0][0] = 2
    game.grid[0][1] = 2
    game.move_cell(0, 1, 0, 0)
    assert game.grid[0][0] == 4
    assert game.grid[0][1] == 0
    assert game.merge_map[0][0] == 1


def test_up():
    # Case 1 - [0, 0, 0, 0]    [2, 4, 0, 0]
    #          [2, 4, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[1][0] = 2
    game.grid[1][1] = 4
    moved = game.up()
    assert moved is True
    assert game.grid[0][0] == 2
    assert game.grid[0][1] == 4

    # Case 2 - [2, 4, 0, 0]    [2, 4, 0, 0]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[0][0] = 2
    game.grid[0][1] = 4
    moved = game.up()
    assert moved is False
    assert game.grid[0][0] == 2
    assert game.grid[0][1] == 4

    # Case 3 - [2, 4, 0, 0]    [4, 4, 0, 0]
    #          [2, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[0][0] = 2
    game.grid[0][1] = 4
    game.grid[1][0] = 2
    moved = game.up()
    assert moved is True
    assert game.grid[0][0] == 4
    assert game.grid[0][1] == 4

    # Case 4 - [2, 4, 0, 0]    [4, 4, 0, 0]
    #          [2, 0, 0, 0] => [8, 0, 0, 0]
    #          [4, 0, 0, 0]    [0, 0, 0, 0]
    #          [4, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[0][0] = 2
    game.grid[1][0] = 2
    game.grid[2][0] = 4
    game.grid[3][0] = 4
    game.grid[0][1] = 4
    moved = game.up()
    assert moved is True
    assert game.grid[0][0] == 4
    assert game.grid[1][0] == 8
    assert game.grid[0][1] == 4

    # Case 5 - [4, 4, 0, 0]    [8, 4, 0, 0]
    #          [4, 0, 0, 0] => [4, 0, 0, 0]
    #          [2, 0, 0, 0]    [0, 0, 0, 0]
    #          [2, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[0][0] = 4
    game.grid[1][0] = 4
    game.grid[2][0] = 2
    game.grid[3][0] = 2
    game.grid[0][1] = 4
    moved = game.up()
    assert moved is True
    assert game.grid[0][0] == 8
    assert game.grid[1][0] == 4
    assert game.grid[0][1] == 4


def test_down():
    # Case 1 - [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [2, 4, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [2, 4, 0, 0]
    game = Game()
    game.grid[1][0] = 2
    game.grid[1][1] = 4
    moved = game.down()
    assert moved is True
    assert game.grid[3][0] == 2
    assert game.grid[3][1] == 4

    # Case 2 - [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [2, 4, 0, 0]    [2, 4, 0, 0]
    game = Game()
    game.grid[3][0] = 2
    game.grid[3][1] = 4
    moved = game.down()
    assert moved is False
    assert game.grid[3][0] == 2
    assert game.grid[3][1] == 4

    # Case 3 - [2, 4, 0, 0]    [0, 0, 0, 0]
    #          [2, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [4, 4, 0, 0]
    game = Game()
    game.grid[0][0] = 2
    game.grid[0][1] = 4
    game.grid[1][0] = 2
    moved = game.down()
    assert moved is True
    assert game.grid[3][0] == 4
    assert game.grid[3][1] == 4

    # Case 4 - [2, 4, 0, 0]    [0, 0, 0, 0]
    #          [2, 0, 0, 0] => [0, 0, 0, 0]
    #          [4, 0, 0, 0]    [4, 0, 0, 0]
    #          [4, 0, 0, 0]    [8, 4, 0, 0]
    game = Game()
    game.grid[0][0] = 2
    game.grid[1][0] = 2
    game.grid[2][0] = 4
    game.grid[3][0] = 4
    game.grid[0][1] = 4
    moved = game.down()
    assert moved is True
    assert game.grid[2][0] == 4
    assert game.grid[3][0] == 8
    assert game.grid[3][1] == 4

    # Case 5 - [4, 4, 0, 0]    [0, 0, 0, 0]
    #          [4, 0, 0, 0] => [0, 0, 0, 0]
    #          [2, 0, 0, 0]    [8, 0, 0, 0]
    #          [2, 0, 0, 0]    [4, 4, 0, 0]
    game = Game()
    game.grid[0][0] = 4
    game.grid[1][0] = 4
    game.grid[2][0] = 2
    game.grid[3][0] = 2
    game.grid[0][1] = 4
    moved = game.down()
    assert moved is True
    assert game.grid[2][0] == 8
    assert game.grid[3][0] == 4
    assert game.grid[3][1] == 4


def test_left():
    # Case 1 - [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [2, 4, 0, 0] => [2, 4, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[1][0] = 2
    game.grid[1][1] = 4
    moved = game.left()
    assert moved is False
    assert game.grid[1][0] == 2
    assert game.grid[1][1] == 4

    # Case 2 - [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 2, 4]    [2, 4, 0, 0]
    game = Game()
    game.grid[3][2] = 2
    game.grid[3][3] = 4
    moved = game.left()
    assert moved is True
    assert game.grid[3][0] == 2
    assert game.grid[3][1] == 4

    # Case 3 - [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 4, 0, 0]    [4, 0, 0, 0]
    #          [2, 2, 0, 0]    [4, 0, 0, 0]
    game = Game()
    game.grid[3][0] = 2
    game.grid[3][1] = 2
    game.grid[2][1] = 4
    moved = game.left()
    assert moved is True
    assert game.grid[2][0] == 4
    assert game.grid[3][0] == 4

    # Case 4 - [0, 4, 0, 0]    [4, 0, 0, 0]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [2, 2, 4, 4]    [4, 8, 0, 0]
    game = Game()
    game.grid[3][0] = 2
    game.grid[3][1] = 2
    game.grid[3][2] = 4
    game.grid[3][3] = 4
    game.grid[0][1] = 4
    moved = game.left()
    assert moved is True
    assert game.grid[0][0] == 4
    assert game.grid[3][0] == 4
    assert game.grid[3][1] == 8

    # Case 5 - [0, 4, 0, 0]    [4, 0, 0, 0]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [4, 4, 2, 2]    [8, 4, 0, 0]
    game = Game()
    game.grid[3][0] = 4
    game.grid[3][1] = 4
    game.grid[3][2] = 2
    game.grid[3][3] = 2
    game.grid[0][1] = 4
    moved = game.left()
    assert moved is True
    assert game.grid[3][0] == 8
    assert game.grid[3][1] == 4
    assert game.grid[0][0] == 4


def test_right():
    # Case 1 - [0, 4, 0, 0]    [0, 0, 0, 4]
    #          [2, 4, 2, 4] => [2, 4, 2, 4]
    #          [4, 4, 2, 2]    [0, 0, 8, 4]
    #          [2, 2, 4, 4]    [0, 0, 4, 8]
    game = Game()
    game.grid[0][1] = 4
    game.grid[1][0] = 2
    game.grid[1][1] = 4
    game.grid[1][2] = 2
    game.grid[1][3] = 4
    game.grid[2][0] = 4
    game.grid[2][1] = 4
    game.grid[2][2] = 2
    game.grid[2][3] = 2
    game.grid[3][0] = 2
    game.grid[3][1] = 2
    game.grid[3][2] = 4
    game.grid[3][3] = 4
    moved = game.right()
    assert moved is True
    assert game.grid[0][3] == 4
    assert game.grid[1][0] == 2
    assert game.grid[1][1] == 4
    assert game.grid[1][2] == 2
    assert game.grid[1][3] == 4
    assert game.grid[2][2] == 8
    assert game.grid[2][3] == 4
    assert game.grid[3][2] == 4
    assert game.grid[3][3] == 8

    # Case 2 - [0, 0, 2, 4]    [0, 0, 2, 4]
    #          [0, 0, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[0][2] = 2
    game.grid[0][3] = 4
    moved = game.right()
    assert moved is False
    assert game.grid[0][2] == 2
    assert game.grid[0][3] == 4


def test_move():
    # Case 1 - [0, 0, 0, 0]    [2, 4, 0, 0]  Plus a random cell
    #          [2, 4, 0, 0] => [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    #          [0, 0, 0, 0]    [0, 0, 0, 0]
    game = Game()
    game.grid[1][0] = 2
    game.grid[1][1] = 4
    game.move("up")
    assert game.grid[0][0] == 2
    assert game.grid[0][1] == 4
    assert len(game.empty_cells()) == 13
