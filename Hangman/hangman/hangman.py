#!/usr/bin/env python3
# filename: hangman.py

"""
hangman.py
~~~~~~~~~~
A program to play the game of Hangman, using random words from
norvig.com/ngrams/sowpods.txt.

To start, execute the following in a shell terminal:
python3 hangman.py
"""

import os
import random
import time


class Hangman:

    def __init__(self, forced_word : str = ''):
        # `word` = the secret word
        self.word = Hangman.clean_input_word(forced_word)
        self.guessed_letters = list()
        self.revealed_positions = [0] * len(self.word)
        self.strikes = 0      # a strike for each incorrect guess
        self.max_strikes = 6  # if changed, must change pictures too

    def show_state(self):
        print(f'(secret) word:      {self.word}')
        print(f'guessed_letters:    {self.guessed_letters}')
        print(f'revealed_positions: {self.revealed_positions}')
        print(f'strikes:            {self.strikes}')
        print(f'max_strikes:        {self.max_strikes}')

    def session(self):
        Hangman.announce_game()
        word_list = Hangman.get_word_list()
        self.game_loop(word_list)
        Hangman.announce_exit()

    def game_loop(self, words : list):
        play_again = Hangman.query_new_game()
        while play_again:
            word = Hangman.select_secret_word(words)
            self.word = Hangman.clean_input_word(word)
            self.update_state_word(self.word)
            self.guess_letters_loop()
            self.show_game_conclusion()
            play_again = Hangman.query_new_game()

    def guess_letters_loop(self):
        while self.strikes < self.max_strikes and \
              sum(self.revealed_positions) < len(self.word):
            self.redraw_game_screen()
            letter = self.query_new_letter()  # user guesses a letter (or quits)
            self.show_letter_result(letter)
            self.update_state_letter(letter)
        self.redraw_game_screen()

    def update_state_word(self, word : str):
        # update after choosing to play a new game, with a new (secret) word
        self.word = word
        self.guessed_letters = list()
        self.revealed_positions = [0] * len(self.word)
        self.strikes = 0

    def redraw_game_screen(self):
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Draw
        print('\n   HANGMAN')
        print(Hangman.hangman_pictures[self.strikes])
        self.show_revealed_letters_graphic()
        print(f'\n  Strikes: {self.strikes}/{self.max_strikes}')
        print(f'  Guesses: ', end='')
        if len(self.guessed_letters) == 0:
            print('(none so far)', end='')
        for i, item in enumerate(self.guessed_letters):
            if i == (len(self.guessed_letters) - 1):
                print(item, end='')
            else:
                print(item + ', ', end='')
        print('')
        #self.show_state()  # for testing

    def show_revealed_letters_graphic(self):
        print('  Secret Word:  ', end='')
        for i, char in enumerate(self.word):
            if self.revealed_positions[i] == 1:
                print(char + ' ', end='')
            else:
                print('_ ', end='')
        print('')

    def query_new_letter(self, forced_letter : str = ''):
        # Query user to enter a new guessed-letter (or user quits)
        valid = False  # assume invalid input (`letter`)
        # To be valid, `letter` must be
        # 1) a single character
        # 2) alpha (alphabetic, not a number or other symbol)
        # 3) new (not an already-guessed letter).
        # An input of `quit` is an exception to these rules,
        # allowing the user to quit and exit the game early.
        while valid == False:
            print('\nEnter a letter or "quit" to exit.')
            if forced_letter is not '':
                letter = forced_letter
            else:
                letter = input('  What\'s your guess? ')
            if letter == 'quit' or letter == 'QUIT':
                Hangman.announce_exit()
                quit()
            if len(letter) == 1 and letter.isalpha() == True:
                letter = str.upper(letter)
                if letter not in self.guessed_letters:
                    valid = True
                else:
                    print('You already guessed that letter. ' + \
                          'Please enter a different letter...')
            else:
                print('Invalid input. ' + \
                      'You must enter a single letter. Please try again...')
        return letter

    def show_letter_result(self, letter : str):
        if letter in self.word:
            print(f'\n  Correct! --- {letter} is in the word!')
        else:
            print(f'\n  Incorrect! - {letter} is *not* in the word!')
        time.sleep(2) # Delay for 2 seconds

    def update_state_letter(self, letter : str):
        # update after guessing another letter of the (secret) word
        self.guessed_letters.append(letter)
        if letter not in self.word:
            self.strikes += 1
        else:
            # record new revealed positions
            for i, char in enumerate(self.word):
                if char == letter:
                    self.revealed_positions[i] = 1  # newly revealed

    def show_game_conclusion(self):
        print(f'\n  The secret word was {self.word}.')
        if sum(self.revealed_positions) == len(self.word):
            print('\n\nYou won! The man is saved, for now. You could try his luck again...')
        else:
            print('\n\nYou lost! The man was hung. But you\'re in luck because we have another man to hang...')

    @staticmethod
    def clean_input_word(string : str):
        if string is not '' and not string.isalpha():
            print(f'\nThe input word entered: {string}')
            print('The input word entered ' + \
                  'is not made of alphabetic characters.')
            print('Continuing with a default word instead...')
            clean_string = 'DEFAULT'
        else:
            clean_string = str.upper(string)
        return clean_string

    @staticmethod
    def announce_game():
        print('\nThis is the game Hangman.')
        print('-- Correctly guess the letters ' + \
              'of the secret word, or else the man gets hung!')

    @staticmethod
    def get_word_list():
        # Could add other functions later that download word list if necessary
        # and let the user know if there's an error in downloading the list.
        with open('./words/sowpods.txt', 'r') as f:
            word_list = f.read().splitlines()
        return word_list

    @staticmethod
    def query_new_game():
        again = input('\nWould you like to play a new game?  ' + \
                      '(Enter y for yes, or n for no.)  ')
        again = str.upper(again)
        if again in {'Y', 'YE', 'YES'}:
            return True
        elif again in {'N', 'NO'}:
            return False
        else:
            print('We\'ll take that as a "no".')
            return False

    @staticmethod
    def select_secret_word(word_list : list):
        word = random.choice(word_list)
        # Could verify word type here, if necessary.
        # Could clean/capitalize word here, if taking from an unclean list.
        return word

    @staticmethod
    def announce_exit():
        print('\nExiting the game.\n')

    # Hangman pictures
    pic0 = ("   _______ \n"
            "   |    |  \n"
            "   |       \n"
            "   |       \n"
            "   |       \n"
            "  _|_______\n")
    pic1 = ("   _______ \n"
            "   |    |  \n"
            "   |       \n"
            "   |    |  \n"
            "   |       \n"
            "  _|_______\n")
    pic2 = ("   _______ \n"
            "   |    |  \n"
            "   |       \n"
            "   |   -|  \n"
            "   |       \n"
            "  _|_______\n")
    pic3 = ("   _______ \n"
            "   |    |  \n"
            "   |       \n"
            "   |   -|- \n"
            "   |       \n"
            "  _|_______\n")
    pic4 = ("   _______ \n"
            "   |    |  \n"
            "   |       \n"
            "   |   -|- \n"
            "   |   /   \n"
            "  _|_______\n")
    pic5 = ("   _______ \n"
            "   |    |  \n"
            "   |       \n"
            "   |   -|- \n"
            "   |   / \\ \n"
            "  _|_______\n")
    pic6 = ("   _______ \n"
            "   |    |  \n"
            "   |    O  \n"
            "   |   -|- \n"
            "   |   / \\ \n"
            "  _|_______\n")
    hangman_pictures = [pic0, pic1, pic2, pic3, pic4, pic5, pic6]



def main():
    hm = Hangman()
    hm.session()


if __name__ == '__main__':
    main()



# Notes
########################################################


# Initial Idea
# ------------
# 1.  Announce game and ask if player would like to play a (new) game or quit.
#     (give option to quit at any time)
# 2.  If playing, ensure file of words is downloaded or download it now.
#     http://norvig.com/ngrams/sowpods.txt
# 3.  Create word list.
# 4.  Select random word.
# 5.  Create game state.
# 6.  Ask for game difficulty (# of tries: default 6?).
# 7.  Select a random word.
# 8.  Have user guess letter.
# 9.  If in word, update game state,
#     inform user of success/failure,
#     display game state.
# 10. If all letters revealed, success
#     else no more chances, failure.
#     display game result.
#     loop back to ask about playing a new game.


# Cleaned-up Version
# ------------------
#
# 0. Initialize Hangman object.
#      (can give a forced_word secret word to do tests)
# 1. Start session,
#    Announce game,
#    (Ensure file of words is downloaded or download it now.)
#      (http://norvig.com/ngrams/sowpods.txt)
#    Create word_list,
#    Ask if player would like to play a (new) game or quit.
#      (give option to quit at any time)
# 2. If playing,
#      Start the game_loop
#    Else
#      Announce exit
# 3. Select random word.
# 4. Etc


