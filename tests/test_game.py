"""
test game models
"""

import unittest
import os


from pycards.models import Game,
from pycards.config import DATA_FOLDER


class TestGame(unittest.TestCase):

    """all test concerning Game. """

    @classmethod
    def setUpClass(cls):
        pass

    def test_init(self):
        """check if instance is created and a file is saved

        """
        files_before = os.listdir(DATA_FOLDER)
        


""" script tests """


if __name__ == '__main__':
    pass
