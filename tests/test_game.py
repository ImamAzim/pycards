"""
test game models
"""

import unittest
import os
import random
import string
import shutil


from pycards.models import Game, GameHandler
from pycards.models.game import SAVED_GAME_FILE_SUFFIX
from pycards.config import DATA_FOLDER


TESTNAME = 'test_game'
card_folder = os.path.dirname(__file__)
RECTO_CARD = 'carreau.png'
VERSO_CARD = 'coeur.png'


class TestGame(unittest.TestCase):

    """all test concerning Game. """

    @classmethod
    def setUpClass(cls):
        cls.game = Game(TESTNAME)
        cls.gamehandler = GameHandler()

    def test_import(self):
        """test if image file is imported

        """
        testname_import = f'{TESTNAME}_import'
        recto = os.path.join(card_folder, RECTO_CARD)
        verso = os.path.join(card_folder, VERSO_CARD)
        self.game.import_card(recto, verso, testname_import)

        path = os.path.join(DATA_FOLDER, TESTNAME)
        try:
            filenames = os.listdir(path)
        except FileNotFoundError:
            filenames = list()
        suffix = RECTO_CARD.split('.')[-1]
        card_name = f'{testname_import}_recto.{suffix}'
        self.assertIn(card_name, filenames)
        filenames = os.listdir(path)
        suffix = VERSO_CARD.split('.')[-1]
        card_name = f'{testname_import}_verso.{suffix}'
        self.assertIn(card_name, filenames)
        self.gamehandler.delete_game(TESTNAME)


class TestGameHandler(unittest.TestCase):

    """all test concerning GameHandler. """

    @classmethod
    def setUpClass(cls):
        cls.game_handler = GameHandler()

    def test_new_init(self):
        """check if instance of Game is created and present

        """
        self.game_handler.new_game(f'{TESTNAME}_newinit')
        self.assertIsNotNone(self.game_handler.game)
        self.assertIsInstance(self.game_handler.game, Game)

    def test_delete_game(self):
        """create files and dir to delete it
        :returns: TODO

        """
        name = f'{TESTNAME}_delete'
        path = os.path.join(DATA_FOLDER, f'{name}.{SAVED_GAME_FILE_SUFFIX}')
        open(path, 'w').close()
        folder_path = os.path.join(DATA_FOLDER, name)
        os.mkdir(folder_path)
        sub_path = os.path.join(folder_path, 'test')
        open(sub_path, 'w').close()

        self.game_handler.delete_game(name)

        filenames = os.listdir(DATA_FOLDER)
        for filename in filenames:
            self.assertNotIn(name, filename)


    # def test_new_save(self):
        # """check if a file and a folder is created for the new game

        # """
        # self.game_handler.new_game(f'{TESTNAME}_newsave')

    @classmethod
    def tearDownClass(cls):
        files = os.listdir(DATA_FOLDER)
        for filename in files:
            if TESTNAME in filename:
                path = os.path.join(DATA_FOLDER, filename)
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)


""" script tests """


if __name__ == '__main__':
    pass
