"""
test game models
"""

import unittest
import os
import random
import string


from pycards.models import Game, GameHandler
from pycards.config import DATA_FOLDER


RANDOM_FN_LENGH = 8

class TestGameHandler(unittest.TestCase):

    """all test concerning GameHandler. """

    @classmethod
    def setUpClass(cls):
        cls.game_handler = GameHandler()
        letters = string.ascii_lowercase
        cls.random_name = ''.join(random.choice(letters) for i in letters)

    def test_new_init(self):
        """check if instance of Game is created and present

        """
        self.game_handler.new_game(self.random_name)
        self.assertIsNotNone(self.game_handler.game)

    @classmethod
    def tearDownClass(cls):
        files = os.listdir(DATA_FOLDER)
        for filename in files:
            if cls.random_name in filename:
                path = os.path.join(DATA_FOLDER, filename)
                os.remove(path)


""" script tests """


if __name__ == '__main__':
    pass
