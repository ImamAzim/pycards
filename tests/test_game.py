
"""
test game models
"""

import unittest


from pycards.models import Game


class TestGame(unittest.TestCase):

    """all test concerning Game. """

    @classmethod
    def setUpClass(cls):
        cls.game = Game()


""" script tests """


if __name__ == '__main__':
    pass
