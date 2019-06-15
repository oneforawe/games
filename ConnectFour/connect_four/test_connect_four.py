#!/usr/bin/env python3
# filename: test_connect_four.py

"""
test_connect_four.py
~~~~~~~~~~~~~~~~~~~~
A script to test the functionality of the code in the file connect_four.py.

To run the tests herein, execute the following in a shell terminal*:
pytest

*And be sure there is an __init__.py file in the same directory.
"""

from .connect_four import ConnectFour


def test_catcher():
    cf = ConnectFour()
    assert cf.catcher == [ [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0] ]


