"""
test game models
"""

import unittest
import os
from pathlib import Path


from pycards.game import Game, GameError, Card
from pycards.game import BOX_FOLDER, DECK_FOLDER
from pycards.config import DATA_FOLDER


TESTNAME = 'test_game'
TESTNAME2 = 'test_game2'
CARD_FOLDER = 'cards'
CARD_FOLDER_PATH = os.path.join(os.path.dirname(__file__), CARD_FOLDER)
RECTO_CARD = 'carreau.png'
VERSO_CARD = 'pic.png'
FALSE_CARD = 'falsecard'


class TestGame(unittest.TestCase):

    """all test concerning Game. """

    def setUp(self):
        """create game instance

        """
        self._game = Game(TESTNAME)
        card_name = 'testcard'
        recto = os.path.join(CARD_FOLDER_PATH, RECTO_CARD)
        verso = os.path.join(CARD_FOLDER_PATH, VERSO_CARD)
        self._test_card = dict(
                recto_path=recto,
                verso_path=verso,
                card_name=card_name,
                )

    def tearDown(self):
        """delete test game from disk
        :returns: TODO

        """
        self._game.delete_game()

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
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
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
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        card = game.get_card(card_name)
        self.assertIsInstance(card, Card)

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertEqual(path, card.path)

    def test_discover_card(self):
        """test discover
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertFalse(os.path.exists(path))
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertFalse(os.path.exists(path))
        self.assertNotIn(card_name, game.box_card_names)

        folder = os.path.join(DATA_FOLDER, TESTNAME, DECK_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))
        self.assertIn(card_name, game.deck_card_names)

    def test_permanent_cards(self):
        """test permanent property

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.lock_card(card_name)

        permanent_cards = game.permanent_cards
        self.assertEqual(1, len(permanent_cards))
        card = permanent_cards[0]
        self.assertIsInstance(card, Card)
        self.assertEqual(card.name, card_name)
        game.unlock_card(card_name)
        permanent_cards = game.permanent_cards
        self.assertEqual(0, len(permanent_cards))

    def test_shuffle(self):
        """test shuffle
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)

        deck = game.shuffle_deck()
        top_card = deck.pop()
        self.assertIsInstance(top_card, Card)

    def test_forget_card(self):
        """test forget

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.forget_card(card_name)

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertTrue(os.path.exists(path))
        self.assertIn(card_name, game.box_card_names)

        folder = os.path.join(DATA_FOLDER, TESTNAME, DECK_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertFalse(os.path.exists(path))
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertFalse(os.path.exists(path))
        self.assertNotIn(card_name, game.deck_card_names)

    def test_destroy(self):
        """test destroy

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.destroy_card(card_name)

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertFalse(os.path.exists(path))
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertFalse(os.path.exists(path))
        self.assertNotIn(card_name, game.box_card_names)

    def test_rotate(self):
        """test rotate card

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.rotate_card(card_name)
        card = game.get_card(card_name)
        self.assertTrue(card.rotate)

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertEqual(path, card.path)

    def test_flip(self):
        """test flip card

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.flip_card(card_name)
        card = game.get_card(card_name)
        self.assertFalse(card.rotate)

        folder = os.path.join(DATA_FOLDER, TESTNAME, BOX_FOLDER)
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = os.path.join(folder, card_fn)
        self.assertEqual(path, card.path)

    def test_delete(self):
        """test delete

        """
        game = self._game
        game.import_card(**self._test_card)
        game.delete_game()

        folder = os.path.join(DATA_FOLDER, TESTNAME)
        self.assertFalse(os.path.exists(folder))

    def test_data_persistance(self):
        """ test if data are preserved between session (autosave) """

        game: Game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        self.assertIn(card_name, game.box_card_names)

        same_game = Game(game.name)
        self.assertIn(card_name, same_game.box_card_names)

        game.discover_card(card_name)
        same_game = Game(game.name)
        self.assertIn(card_name, same_game.deck_card_names)

        game.lock_card(card_name)
        same_game = Game(game.name)
        self.assertTrue(same_game.is_card_permanent(card_name))

        game.destroy_card(card_name)
        same_game = Game(game.name)
        with self.assertRaises(GameError):
            same_game.get_card(card_name)

    def test_get_saved_games(self):
        """test get saved games

        """
        saved_games = Game.get_saved_game()
        self.assertIn(TESTNAME, saved_games)

    def test_new_load_game(self):
        """test new and load

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.new(TESTNAME2)
        self.assertEqual(game.name, TESTNAME2)
        self.assertNotIn(card_name, game.box_card_names)
        game.load(TESTNAME)

        self.assertEqual(game.name, TESTNAME)
        self.assertIn(card_name, game.box_card_names)

        game.load(TESTNAME2)
        game.delete_game()
        game.load(TESTNAME)

    def test_get_card_pile(self):
        """
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        with self.assertRaises(GameError):
            pile = self._game.get_card_pile(card_name)

        game.discover_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'discard')

        game.lock_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'permanent')

        game.unlock_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'discard')


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
        self.assertFalse(card.is_locked)

        card = Card(name, recto, verso, 1)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, recto)
        self.assertTrue(card.rotate)
        self.assertFalse(card.is_locked)

        card = Card(name, recto, verso, 2, is_locked=True)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, verso)
        self.assertTrue(card.rotate)
        self.assertTrue(card.is_locked)

        card = Card(name, recto, verso, 3, is_locked=True)
        self.assertEqual(card.name, name)
        self.assertEqual(card.path, verso)
        self.assertFalse(card.rotate)
        self.assertTrue(card.is_locked)


""" script tests """


if __name__ == '__main__':
    pass
