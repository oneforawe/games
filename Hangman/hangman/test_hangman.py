#!/usr/bin/env python3
# filename: test_hangman.py

"""
test_hangman.py
~~~~~~~~~~~~~~~
A script to test the functionality of the code in the file hangman.py.

To run the tests herein, execute the following in a shell terminal*:
pytest

*And be sure there is an __init__.py file in the same directory.
"""

from .hangman import Hangman


# Initialization
# -----------------------------------------------------------------------------

# Has to be re-written to account for new behavior of program.
#def test_initialize_forced_word_0a():
#    hm = Hangman('not valid')
#    assert hm.word == ''

# Has to be re-written to account for new behavior of program.
#def test_initialize_forced_word_0b():
#    hm = Hangman('A1')
#    assert hm.word == ''

def test_initialize_forced_word_1():
    hm = Hangman('HELLO')
    assert hm.word == 'HELLO'

def test_initialize_forced_word_2():
    hm = Hangman('hello')
    assert hm.word == 'HELLO'

def test_initialize_guessed_letters():
    hm = Hangman('hello')
    assert hm.guessed_letters == list()

def test_initialize_revealed_positions():
    hm = Hangman('hello')
    assert hm.revealed_positions == [0, 0, 0, 0, 0]

def test_initialize_strikes():
    hm = Hangman('hello')
    assert hm.strikes == 0

def test_initialize_max_strikes():
    hm = Hangman('hello')
    # could change max_strikes, but would need to change number of pictures too
    assert hm.max_strikes == 6


# revealed positions
# -----------------------------------------------------------------------------

def test_revealed_positions():
    hm = Hangman('hello')
    hm.update_state_letter('L')
    assert hm.revealed_positions== [0, 0, 1, 1, 0]


# strike out
# -----------------------------------------------------------------------------

def test_strike_out():
    hm = Hangman('z')
    letter = hm.query_new_letter('a')
    hm.update_state_letter(letter) # strike
    letter = hm.query_new_letter('b')
    hm.update_state_letter(letter) # strike
    letter = hm.query_new_letter('c')
    hm.update_state_letter(letter) # strike
    letter = hm.query_new_letter('d')
    hm.update_state_letter(letter) # strike
    letter = hm.query_new_letter('e')
    hm.update_state_letter(letter) # strike
    letter = hm.query_new_letter('f')
    hm.update_state_letter(letter) # strike
    assert hm.strikes == 6


# one wrong letter repeated, only one strike
# -----------------------------------------------------------------------------

"""
# Hangman.query_new_letter() doesn't allow the same letter to be entered;
# it interactively asks for a new letter.  So, with this behavior, I can't
# automatically use it in a test here.

def test_same_letter_guess_no_strike():
    hm = Hangman('EE')
    letter = hm.query_new_letter('d')
    hm.update_state_letter(letter) # strike
    letter = hm.query_new_letter('d')
    hm.update_state_letter(letter) # already guessed, no strike
    assert hm.strikes == 1
"""

