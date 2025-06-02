"""
test game models
"""

import unittest
import os
import shutil


from pycards.game import Game, GameHandler, GameError, Card
from pycards.game import SAVED_GAME_FILE_SUFFIX, BOX_FOLDER, DECK_FOLDER
from pycards.config import DATA_FOLDER


TESTNAME = 'test_game'
CARD_FOLDER = 'cards'
CARD_FOLDER_PATH = os.path.join(os.path.dirname(__file__), CARD_FOLDER)
RECTO_CARD = 'carreau.png'
VERSO_CARD = 'pic.png'
FALSE_CARD = 'falsecard'


class TestGame(unittest.TestCase):

    """all test concerning Game. """

    @classmethod
    def setUpClass(cls):
        cls._gamehandler = GameHandler()

    def setUp(self):
        """create game instance

        """
        self._game = Game(TESTNAME)
        card_name = 'testcard'
        recto = os.path.join(CARD_FOLDER_PATH, RECTO_CARD)
        verso = os.path.join(CARD_FOLDER_PATH, VERSO_CARD)
        self._test_card = dict(recto_path=recto, verso_path=verso, card_name=card_name)

    def tearDown(self):
        """delete test game from disk
        :returns: TODO

        """
        self._gamehandler.delete_game(TESTNAME)

    def test_property(self):
        """check attibutes of games
        :returns: TODO

        """
        game = self._game
        self.assertEqual(game.name, TESTNAME)
        self.assertSequenceEqual(game.box_card_names, ())
        self.assertSequenceEqual(game.deck_card_names, ())

    def test_import(self):
        """test if image file is imported

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = RECTO_CARD.split('.')[-1]
        card_fn = f'{card_name}_recto.{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))
        suffix = VERSO_CARD.split('.')[-1]
        card_fn = f'{card_name}_verso.{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))

        self.assertIn(card_name, game.box_card_names)

    def test_import_error(self):
        """ check raise error if file is not an img """
        game = self._game
        path = os.path.join(CARD_FOLDER_PATH, FALSE_CARD)
        with self.assertRaises(GameError):
            game.import_card(path, path)

    def test_import_folder(self):
        """test import folder

        """
        game = self._game
        folder = CARD_FOLDER_PATH
        game.import_cards_folder(folder)
        self.assertEqual(len(game.box_card_names), 1)

    def test_getcard(self):
        """test get card
        :returns: TODO

        """
        game = self._game
        folder = CARD_FOLDER_PATH
        game.import_cards_folder(folder)
        for card_name in game.box_card_names:
            card = game.get_card(card_name)
            self.assertIsInstance(card, Card)

    # def test_discover_card(self):
        # """test discover
        # :returns: TODO

        # """
        # game = self._game
        # card_name = 'testcard'
        # recto = os.path.join(CARD_FOLDER_PATH, RECTO_CARD)
        # verso = os.path.join(CARD_FOLDER_PATH, VERSO_CARD)
        # game.import_card(recto, verso, card_name)
        # game.discover_card(card_name)

    # def test_permanent_cards(self):
        # """test permanent property

        # """
        # game = self.game
        # card_name = 'testcard'
        # recto = os.path.join(CARD_FOLDER_PATH, RECTO_CARD)
        # verso = os.path.join(CARD_FOLDER_PATH, VERSO_CARD)
        # game.import_card(recto, verso, card_name)
        # game.discover_card(card_name)
        # game.lock_card(card_name)

        # permanent_cards = game.permanent_cards
        # self.assertEqual(1, len(permanent_cards))
        # card = permanent_cards[0]
        # self.assertIsInstance(card, Card)
        # self.assertEqual(card.name, card_name)
        # game.unlock_card(card_name)
        # permanent_cards = game.permanent_cards
        # self.assertEqual(0, len(permanent_cards))


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


class TestCard(unittest.TestCase):

    """all test concerning Card. """

    def test_init(self):
        """test if it create Card object with correct parameters
        """
        recto = os.path.join(CARD_FOLDER_PATH, RECTO_CARD)
        verso = os.path.join(CARD_FOLDER_PATH, VERSO_CARD)
        name = 'test_card'

        card = Card(name, recto, verso, 0)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, recto)
        self.assertFalse(card.rotate)

        card = Card(name, recto, verso, 1)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, recto)
        self.assertTrue(card.rotate)

        card = Card(name, recto, verso, 2)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, verso)
        self.assertTrue(card.rotate)

        card = Card(name, recto, verso, 3)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, verso)
        self.assertFalse(card.rotate)

""" script tests """


if __name__ == '__main__':
    pass
