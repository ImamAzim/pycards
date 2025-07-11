"""
test game models
"""

import unittest
from pathlib import Path


from pycards.game import Game, GameError, Card
from pycards.game import BOX_FOLDER, DECK_FOLDER
from pycards.config import DATA_FOLDER


TESTNAME = 'test_game'
TESTNAME2 = 'test_game2'
CARD_FOLDER = 'cards'
RECTO_CARD = 'carreau.png'
VERSO_CARD = 'pic.png'
FALSE_CARD = 'falsecard'
STICKER_FN = 'sticker_test.jpg'

TEST_FOLDER_PATH = Path(__file__).parent / CARD_FOLDER
STICKER_FP = TEST_FOLDER_PATH / STICKER_FN


class TestGame(unittest.TestCase):

    """all test concerning Game. """

    def setUp(self):
        """create game instance

        """
        self._game = Game(TESTNAME)
        card_name = 'testcard'
        recto = TEST_FOLDER_PATH / RECTO_CARD
        verso = TEST_FOLDER_PATH / VERSO_CARD
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
        self.assertEqual(game.stickers, dict())

    def test_import(self):
        """test if image file is imported

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertTrue(path.exists())
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertTrue(path.exists())

        self.assertIn(card_name, game.box_card_names)

    def test_import_sticker(self):
        game = self._game
        sticker_name = 'sticker_test_name'
        game.import_sticker(STICKER_FP, sticker_name)
        suffix = STICKER_FP.suffix
        expected_fn = sticker_name + suffix
        expected_fp: Path = DATA_FOLDER / TESTNAME / BOX_FOLDER / expected_fn
        self.assertTrue(expected_fp.exists())
        self.assertIn(sticker_name, game.stickers)
        self.assertTrue(expected_fp.samefile(game.stickers[sticker_name]))

    def test_import_error(self):
        """ check raise error if file is not an img """
        game = self._game
        path = TEST_FOLDER_PATH / FALSE_CARD
        with self.assertRaises(GameError):
            game.import_card(path, path)

    def test_import_folder(self):
        """test import folder

        """
        game = self._game
        folder = TEST_FOLDER_PATH
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

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertTrue(path.samefile(card.path))

    def test_get_top_card(self):
        """test draw top card
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        card = game.get_card(card_name)
        game.put_card_in_draw_pile(card_name)
        card_top = game.get_draw_pile_top_card()
        self.assertEqual(card.name, card_top.name)

    def test_discover_card(self):
        """test discover
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertFalse(path.exists())
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertFalse(path.exists())
        self.assertNotIn(card_name, game.box_card_names)

        folder = DATA_FOLDER / TESTNAME / DECK_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertTrue(path.exists())
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertTrue(path.exists())
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
        self.assertIn(card_name, permanent_cards)
        card = permanent_cards[card_name]
        self.assertIsInstance(card, Card)
        self.assertEqual(card.name, card_name)
        game.unlock_card(card_name)
        permanent_cards = game.permanent_cards
        self.assertNotIn(card_name, permanent_cards)

    def test_discarded_cards(self):
        """test discarded card disct

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)

        discarded = game.discarded_cards
        self.assertIn(card_name, discarded)
        card = discarded[card_name]
        self.assertIsInstance(card, Card)
        self.assertEqual(card.name, card_name)
        game.put_card_in_draw_pile(card_name)
        discarded = game.discarded_cards
        self.assertNotIn(card_name, discarded)

    def test_in_play_cards(self):
        """test in play card disct

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.play_card(card_name)

        in_play = game.in_play_cards
        self.assertIn(card_name, in_play)
        card = in_play[card_name]
        self.assertIsInstance(card, Card)
        self.assertEqual(card.name, card_name)
        game.put_card_in_draw_pile(card_name)
        in_play = game.in_play_cards
        self.assertNotIn(card_name, in_play)

    def test_draw_pile(self):
        """test draw pile

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.put_card_in_draw_pile(card_name)

        game.shuffle_draw_pile()

        draw_pile = game.draw_pile_cards
        self.assertNotIn(card_name, draw_pile)
        obfuscated_card_name = draw_pile[0]
        real_card_name = game.get_real_card_name(obfuscated_card_name)
        self.assertEqual(card_name, real_card_name)
        game.play_card(real_card_name)
        draw_pile = game.draw_pile_cards
        self.assertEqual(0, len(draw_pile))

        game.set_always_visible(card_name)
        game.put_card_in_draw_pile(card_name)
        draw_pile = game.draw_pile_cards
        self.assertIn(card_name, draw_pile)
        obfuscated_card_name = draw_pile[0]
        real_card_name = game.get_real_card_name(obfuscated_card_name)
        self.assertEqual(card_name, real_card_name)
        game.play_card(real_card_name)
        draw_pile = game.draw_pile_cards
        self.assertEqual(0, len(draw_pile))

        game.shuffle_draw_pile()

    def test_forget_card(self):
        """test forget

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.forget_card(card_name)

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertTrue(path.exists())
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertTrue(path.exists())
        self.assertIn(card_name, game.box_card_names)

        folder = DATA_FOLDER / TESTNAME / DECK_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertFalse(path.exists())
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertFalse(path.exists())
        self.assertNotIn(card_name, game.deck_card_names)

    def test_destroy(self):
        """test destroy

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.destroy_card(card_name)

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertFalse(path.exists())
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertFalse(path.exists())
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

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(RECTO_CARD).suffix
        card_fn = f'{card_name}_recto{suffix}'
        path = folder / card_fn
        self.assertTrue(path.samefile(card.path))

    def test_flip(self):
        """test flip card

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.flip_card(card_name)
        card = game.get_card(card_name)
        self.assertFalse(card.rotate)

        folder = DATA_FOLDER / TESTNAME / BOX_FOLDER
        suffix = Path(VERSO_CARD).suffix
        card_fn = f'{card_name}_verso{suffix}'
        path = folder / card_fn
        self.assertTrue(path.samefile(card.path))

    def test_delete(self):
        """test delete

        """
        game = self._game
        game.import_card(**self._test_card)
        game.delete_game()

        folder = DATA_FOLDER / TESTNAME
        self.assertFalse(folder.exists())

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
        self.assertEqual(same_game.get_card_pile(card_name), 'permanent')

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
        with self.assertRaises(GameError):
            self._game.play_card(card_name)

        game.discover_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'discard')

        game.lock_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'permanent')
        with self.assertRaises(GameError):
            self._game.play_card(card_name)

        game.unlock_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'discard')

        self._game.play_card(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'in_play')

        self._game.discard(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'discard')

        self._game.put_card_in_draw_pile(card_name)
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'draw')

        self._game.play_first_card()
        pile = self._game.get_card_pile(card_name)
        self.assertEqual(pile, 'in_play')

    def test_discard_all(self):
        """
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.play_card(card_name)
        game.discard_all_cards_in_play()
        discarded = game.discarded_cards
        self.assertIn(card_name, discarded)

    def test_shuffle_all(self):
        """
        :returns: TODO

        """
        game = self._game
        game.import_card(**self._test_card)
        card_name = self._test_card['card_name']
        game.discover_card(card_name)
        game.shuffle_back_all_discarded()
        draw_pile = game.draw_pile_cards
        obf = draw_pile[0]
        real_card_name = game.get_real_card_name(obf)
        self.assertEqual(card_name, real_card_name)


class TestCard(unittest.TestCase):

    """all test concerning Card. """

    def test_init(self):
        """test if it create Card object with correct parameters
        """
        recto = TEST_FOLDER_PATH / RECTO_CARD
        verso = TEST_FOLDER_PATH / VERSO_CARD
        name = 'test_card'

        card = Card(name, recto, verso, 0)
        self.assertEqual(card.name, name)
        self.assertTrue(recto.samefile(card.path))
        self.assertFalse(card.rotate)

        card = Card(name, recto, verso, 1)
        self.assertEqual(card.name, name)
        self.assertTrue(recto.samefile(card.path))
        self.assertTrue(card.rotate)

        card = Card(name, recto, verso, 2)
        self.assertEqual(card.name, name)
        self.assertTrue(verso.samefile(card.path))
        self.assertTrue(card.rotate)

        card = Card(name, recto, verso, 3)
        self.assertEqual(card.name, name)
        self.assertTrue(verso.samefile(card.path))
        self.assertFalse(card.rotate)


""" script tests """


if __name__ == '__main__':
    unittest.main()
    pass
