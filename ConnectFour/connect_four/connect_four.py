#!/usr/bin/env python3
# filename: connect_four.py

"""
connect_four.py
~~~~~~~~~~~~~~~
A program to play the game Connect Four.  Two players drop pucks of
their own color (or number-label) into slots/columns of a "catcher",
where the pucks are visible to the players and stack upon each other
in the columns, arranged in a grid-like pattern across rows and diag-
onals as well as in the columns.  The first player to get four of
thon's own pucks in a line (horizontal, vertical, or diagonal) wins.
A full catcher with no four-puck streaks results in a stale-mate.

To start, execute the following in a shell terminal:
python3 connect_four.py
"""

# TODO: clean input for columns
# TODO: write tests in test_connect_four

import os


class ConnectFour:

    def __init__(self, height : int = 6, base: int = 7):
        height, base = ConnectFour.clean_height_base_input(height, base)
        # TODO: clean input (needs to be positive integer, can't be zero)
        # Note regarding the catcher:
        # the 0 row is the bottom row, the (height-1) row is the top row
        # the 0 col is the left row, the (base-1) col is the right col
        self.base = base      # = number of columns
        self.height = height  # = number of rows
        self.catcher = [[0 for _ in range(base)] for _ in range(height)]
        self.active_player = 0
        self.winner = -1  # {-1:N/A, 0:stale-mate, 1:player-1, 2:player-2}
        self.paths = { 'cols'   : self.path_generator_cols(),
                       'rows'   : self.path_generator_rows(),
                       'ndiags' : self.path_generator_ndiags(),
                       'pdiags' : self.path_generator_pdiags() }

    def reset_for_new_game(self, base = None, height = None):
        # leave base and height the same
        if base is None:
            base = self.base
        if height is None:
            height = self.height
        self.base = base
        self.height = height
        self.catcher = [[0 for _ in range(base)] for _ in range(height)]
        self.active_player = 0
        self.winner = -1  # {-1:N/A, 0:stale-mate, 1:player-1, 2:player-2}

    def show_state(self):
        print(f'self.base = {self.base}')
        print(f'self.height = {self.height}')
        print(f'self.catcher = {self.catcher}')
        print(f'self.active_player = {self.active_player}')
        print(f'self.winner = {self.winner}')

    def session(self):
        ConnectFour.announce_game()
        self.game_loop()
        ConnectFour.announce_exit()

    def game_loop(self):
        play_again = ConnectFour.query_new_game()
        while play_again:
            self.reset_for_new_game()
            self.player_turn_loop()
            play_again = ConnectFour.query_new_game()

    def player_turn_loop(self):
        while not self.game_over():
            self.switch_player()
            self.redraw_screen()
            self.query_player_for_valid_col()
        self.redraw_screen()
        self.show_game_conclusion()

    def game_over(self) -> bool:
        # calculate whether there's a four-in-a-row streak
        # if there is, return true
        # set `self.winner` to winning mode or leave at -1 if game not over
        # 1. Check for a winner
        for direction in self.paths:
            if self.check_for_win(direction):
                return True
        # 2. Check for a state-mate (catcher full), given no winner was found
        if self.check_for_full_catcher():
            return True
        return False

    def check_for_win(self, direction : str) -> bool:
        # direction determines which "paths" to traverse
        # (in the diagonal paths, the paths have different length)
        # for each path, keep track of
        #  1) player with potential streak
        #  2) number of pucks in current streak (if any)
        for path in self.paths[direction]:
            counter = 0  # counting same-player pucks in a streak
            player_with_streak = 0
            for spot in path:
                value = self.catcher[spot[0]][spot[1]]
                if value in {1, 2}:
                    if player_with_streak == value:
                        # additional puck in a streak
                        counter += 1
                    else:
                        # first puck in a streak
                        player_with_streak = value
                        counter = 1
                else:
                    player_with_streak = 0
                    streak_counter = 0
                if counter == 4:
                    # connect four!
                    self.winner = player_with_streak
                    return True
        return False

    def check_for_full_catcher(self) -> bool:
        # Check for a state-mate (catcher full), given that no winner was found
        # Search for a single zero-value in the catcher (if none return True)
        # Only need to check the top row
        for col in range(0, self.base):
            if self.catcher[self.height - 1][col] == 0:
                return False
        self.winner = 0  # stale-mate
        return True

    def switch_player(self):
        print(self.active_player)
        if self.active_player == 2 or self.active_player == 0:
            self.active_player = 1
        elif self.active_player == 1:
            self.active_player = 2
        print(self.active_player)

    def redraw_screen(self):
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Draw
        print('\n  CONNECT FOUR\n')
        self.show_catcher_graphic()

    def query_player_for_valid_col(self):
        # query active player for a valid column to drop a puck
        valid = False
        print('\nPlease enter a column number ' + \
              f'(from 1 to {self.base}) to drop your puck into that column.')
        print('(You can also enter "quit" to exit the game.)\n')
        while valid == False:
            col = input(f'Player {self.active_player}, which column? ')
            if col == 'quit' or col == 'QUIT':
                ConnectFour.announce_exit()
                quit()
            if col.isdigit() and int(col) in range(1, self.base + 1):
                col = int(col)
                valid = self.try_to_place_puck(col)
            else:
                print('Invalid input. ' + \
                      'Please enter a number in the proper range.\n')
        return col

    def try_to_place_puck(self, col):
        # the 0 row is the bottom row, the 3 row is the top row
        # the player has selected column `col`
        # we need to determine if this is a valid place to place the puck
        valid = False
        row = 0
        for row in range(self.height):
            if valid == False and self.catcher[row][col-1] == 0:
                self.catcher[row][col-1] = self.active_player
                valid = True
        if valid == False:
            print('That column is full. Please pick a different column.\n')
        return valid

    def show_catcher_graphic(self):
        for row in reversed(range(self.height)):
            print(f'  {self.catcher[row]}')
        print('')

    def show_game_conclusion(self):
        # winner: 0 (stale-mate), 1, 2
        if self.winner == 0:
            print('\n~~ Stale-mate! ~~  Looks like you players were evenly matched!\n')
        if self.winner == 1:
            print('\n~~ Connect Four! ~~  Player 1 is the winner!\n')
        if self.winner == 2:
            print('\n~~ Connect Four! ~~  Player 2 is the winner!\n')

    def path_generator_cols(self):
        # Collecting all the "cols": downward column paths
        paths = []
        for col in range(0, self.base):
            path = []
            for row in reversed(range(0, self.height)):
                spot = (row, col)
                path.append(spot)
            paths.append(path)
        return paths

    def path_generator_rows(self):
        # Collecting all the "rows": leftward row paths
        paths = []
        for row in range(0, self.height):
            path = []
            for col in range(0, self.base):
                spot = (row, col)
                path.append(spot)
            paths.append(path)
        return paths

    def path_generator_ndiags(self):
        # Collecting all the "ndiags":
        #  the negatively-sloped left-to-right diagonal paths
        paths = []
        # Paths starting from the left side (and top, for last path):
        col_start = 0
        row_start_min = 4 - 1  # (need space for four pucks)
        row_start_max = self.height - 1
        for row_start in range(row_start_min, row_start_max + 1):
            path = []
            row = row_start
            col = col_start
            while row >= 0 and col < self.base:
                spot = (row, col)
                path.append(spot)
                row -= 1
                col += 1
            paths.append(path)
        # Paths starting from the top (except the first, see above):
        row_start = self.height - 1
        col_start_min = 1
        col_start_max = self.base - 1 - 3  # (need space for four pucks)
        for col_start in range(col_start_min, col_start_max + 1):
            path = []
            row = row_start
            col = col_start
            while row >= 0 and col < self.base:
                spot = (row, col)
                path.append(spot)
                row -= 1
                col += 1
            paths.append(path)
        return paths

    def path_generator_pdiags(self):
        # Collecting all the "pdiags":
        #  the positively-sloped left-to-right diagonal paths
        paths = []
        # Paths starting from the left side (and bottom, for last path):
        col_start = 0
        row_start_max = self.height - 1 - 3 # (need space for four pucks)
        row_start_min = 0
        for row_start in reversed(range(row_start_min, row_start_max + 1)):
            path = []
            row = row_start
            col = col_start
            while row < self.height and col < self.base:
                spot = (row, col)
                path.append(spot)
                row += 1
                col += 1
            paths.append(path)
        # Paths starting from the bottom (except the first, see above):
        row_start = 0
        col_start_min = 1
        col_start_max = self.base - 1 - 3  # (need space for four pucks)
        for col_start in range(col_start_min, col_start_max + 1):
            path = []
            row = row_start
            col = col_start
            while row < self.height and col < self.base:
                spot = (row, col)
                path.append(spot)
                row += 1
                col += 1
            paths.append(path)
        return paths

    @staticmethod
    def clean_height_base_input(height : int, base : int):
        if not isinstance(height, int) and height < 1:
            print('The catcher height input must be a non-zero positive ' + \
                  'integer; using a default value.')
            height = 6
        if not isinstance(base, int) and height < 1:
            print('The catcher base input must be a non-zero positive ' + \
                  'integer; using a default value.')
            base = 7
        return height, base

    @staticmethod
    def announce_game():
        print('\nThis is the game Connect Four.')
        print('-- Two players drop their own pucks into a vertical grid')
        print('   arrangement and attempt to get four pucks in a line')
        print('   (horizontal, vertical, or diagonal). The first player to')
        print('   "connect four" wins.')

    @staticmethod
    def query_new_game():
        again = input('\nWould you like to play a new game? ' + \
                      '(Enter y for yes, n for no.) ')
        again = str.upper(again)
        if again in {'Y', 'YE', 'YES'}:
            return True
        elif again in {'N', 'NO'}:
            return False
        else:
            print('We\'ll take that as a "no".')
            return False

    @staticmethod
    def announce_exit():
        print('\nExiting the game.')


def show_shape(arbitrary_list):
    shape(arbitrary_list)
    print('')

def shape(arbitrary_list):
    print(f'[ {len(arbitrary_list)}: ', end='')
    for el in arbitrary_list:
        if isinstance(el, list):
            shape(el)
        else:
            print('* ', end='')
    print(']', end='')




def main():
    cf = ConnectFour()
    cf.session()


if __name__ == '__main__':
    main()




# Notes
# ==================
# catcher / board
# base / rows
# height / columns/slots
# spots
# puck / disc
# streak
# path

