import os
import shutil
from pathlib import Path
import random
from typing import Literal


import filetype
from varboxes import VarBox


from pycards.config import DATA_FOLDER
from pycards.interfaces import BaseCard


SAVED_GAME_FILE_SUFFIX = 'json'
BOX_FOLDER = 'box'
DECK_FOLDER = 'deck'
TEMP_NAME = 'tmp'

DRAW_PILE_NAME = 'draw'
IN_PLAY_PILE_NAME = 'in_play'
DISCARD_PILE_NAME = 'discard'
PERMANENT_PILE_NAME = 'permanent'


class Card(BaseCard):

    """card object for a given orientation"""

    @property
    def name(self) -> str:
        """card name"""
        return self._name

    @property
    def path(self) -> str:
        """path to img file"""
        return self._path

    @property
    def rotate(self) -> bool:
        """specify if img need to be rotated by 180 deg"""
        return self._rotate

    def __init__(
            self,
            card_name: str,
            recto_path: str,
            verso_path: str,
            orientation: int,
            **others,
            ):
        """create a card obj and get img_file to use and rotation

        :card_name: identy card
        :recto_path: path to recto img
        :verso_path: path to verso img
        :orientation: 0(top recto), 1(down recto), 2(down verso), or
        3(top verso)

        """
        self._name = card_name
        if (orientation == 0) | (orientation == 1):
            self._path = recto_path
        else:
            self._path = verso_path
        if (orientation == 1) | (orientation == 2):
            self._rotate = True
        else:
            self._rotate = False


class GameError(Exception):
    pass


class Game(object):

    """Game class to handle the deck and the cards box"""

    _saved_games = VarBox(app_name='saved_games')
    if not hasattr(_saved_games, 'names'):
        _saved_games.names = list()

    @classmethod
    def get_saved_game(cls) -> (str):
        """look for all saved games on disk
        :returns: list of saved games names

        """
        saved_games = tuple(cls._saved_games.names)
        return saved_games

    @property
    def name(self) -> str:
        """name of the game"""
        return self._name

    @property
    def box_card_names(self) -> list:
        """return an ordered list of the card names in the box"""
        return sorted(self._box.keys())

    @property
    def deck_card_names(self) -> list:
        """return an ordered list of the card names in the deck"""
        return sorted(self._deck.keys())

    @property
    def permanent_cards(self) -> dict[str, Card]:
        """get a list of permanent cards from the deck"""
        permanent_cards = {
                card_name: self.get_card(card_name)
                for card_name, card in self._deck.items()
                if card.get('pile') == self._PERMANENT_PILE}
        return permanent_cards

    @property
    def in_play_cards(self) -> dict[str, Card]:
        """get a list of in-play cards from the deck"""
        in_play = {
                card_name: self.get_card(card_name)
                for card_name, card in self._deck.items()
                if card.get('pile') == self._IN_PLAY_PILE}
        return in_play

    @property
    def discarded_cards(self) -> dict[str, Card]:
        """get a list of discarded cards from the deck"""
        discarded = {
                card_name: self.get_card(card_name)
                for card_name, card in self._deck.items()
                if card.get('pile') == self._DISCARD_PILE}
        return discarded

    @property
    def draw_pile_cards(self) -> list[str]:
        """get a tuple of the draw pile. names are obfuscated"""
        return tuple(self._draw_pile)

    def get_real_card_name(self, obfuscated_card_name: str) -> str:
        """reveal the card name when hidden in the draw pile

        :obfuscated_card_name:
        :returns:

        """
        return self._draw_cards_real_name.get(obfuscated_card_name)

    _DRAW_PILE = DRAW_PILE_NAME
    _IN_PLAY_PILE = IN_PLAY_PILE_NAME
    _DISCARD_PILE = DISCARD_PILE_NAME
    _PERMANENT_PILE = PERMANENT_PILE_NAME
    _ALWAYS_VISIBLE = 'always_visible'

    def __init__(self, name: str = TEMP_NAME):
        if name in self._saved_games.names:
            self.load(name)
        else:
            self.new(name)

    def new(self, name: str):
        """create a new game

        :name: should not be already present, else will raise error

        """
        if name not in self._saved_games.names:
            if name != TEMP_NAME:
                self._saved_games.names.append(name)
                self._saved_games.save()
            self._change_name(name)
        else:
            raise GameError('there is already a saved game with this name')

    def load(self, name: str):
        """load a previousely saved game

        :name: there must be a game that was saved with that name

        """
        if name in self._saved_games.names:
            self._change_name(name)
        else:
            raise GameError('there is no saved game with this name')

    def _change_name(self, name: str):
        """update folder and other data from game name

        :name:

        """
        self._name = name
        self._game_data_folder = os.path.join(DATA_FOLDER, self.name)
        self._box_folder = os.path.join(self._game_data_folder, BOX_FOLDER)
        os.makedirs(self._box_folder, exist_ok=True)
        self._deck_folder = os.path.join(self._game_data_folder, DECK_FOLDER)
        os.makedirs(self._deck_folder, exist_ok=True)

        self._varbox = self._create_varbox(name)

        self._box = self._varbox.box
        self._deck = self._varbox.deck
        self._draw_pile = self._varbox.draw_pile
        self._draw_cards_real_name = self._varbox.draw_cards_real_name
        varboxobf = self._varbox.draw_cards_obfuscate_name
        self._draw_cards_obfuscate_name = varboxobf
        self._all_cards = dict(box=self._box, deck=self._deck)

    def _create_varbox(self, name) -> VarBox:
        """create varbox or load an existing one and add
        attributes (if not presents) to store permanent data

        :name: game
        :returns: varbox

        """
        varbox = VarBox(app_name=name)

        if not hasattr(varbox, 'box'):
            varbox.box = dict()
        if not hasattr(varbox, 'deck'):
            varbox.deck = dict()
        if not hasattr(varbox, 'draw_pile'):
            varbox.draw_pile = list()
        if not hasattr(varbox, 'draw_cards_real_name'):
            varbox.draw_cards_real_name = dict()
        if not hasattr(varbox, 'draw_cards_obfuscate_name'):
            varbox.draw_cards_obfuscate_name = dict()
        return varbox

    def _reset_varbox(self):
        """reset all the data of the current varbox

        """
        varbox = self._varbox
        varbox.box = dict()
        varbox.deck = dict()
        varbox.draw_pile = list()
        varbox.draw_cards_real_name = dict()
        varbox.draw_obfuscate_real_name = dict()

    def get_card_pile(self, card_name) -> Literal[
            'draw', 'discard', 'permanent', 'in_play']:
        """find in which pile is located the card of the deck

        :card_name:
        :returns: on of [draw, in_play, permanent, discard]

        """
        if card_name in self.deck_card_names:
            card = self._deck.get(card_name)
            return card.get('pile')
        else:
            raise GameError('card is not in the deck')

    def delete_game(self) -> str:
        """remove all saved cards and folders from disk. a config file will
        still be present.
        :return: path of the empty config file

        """
        path = self._game_data_folder
        if os.path.exists(path):
            shutil.rmtree(path)
        self._reset_varbox()
        varbox_path = self._varbox.get_path()
        os.remove(varbox_path)
        saved_games: list = self._saved_games.names
        if self.name != TEMP_NAME:
            saved_games.remove(self.name)
            self._saved_games.save()
        self._change_name(TEMP_NAME)

    def import_card(
            self,
            recto_path: str,
            verso_path: str,
            card_name: str = None,
            ):
        """import a card and put it in the game folder.

        :recto_path: img file of recto
        :verso_path: img file of verso
        :card_name: if None take value of recto filename
        """

        if not filetype.is_image(recto_path):
            raise GameError('recto file is not an image')
        if not filetype.is_image(verso_path):
            raise GameError('recto file is not an image')

        ext = Path(recto_path).suffix
        if card_name is None:
            card_name = Path(recto_path).stem

        if self._check_card_in_game(card_name):
            raise GameError('card already in box or in deck')

        recto_name = f'{card_name}_recto{ext}'
        verso_name = f'{card_name}_verso{ext}'
        src_recto = recto_path
        dst_recto = os.path.join(self._box_folder, recto_name)
        src_verso = verso_path
        dst_verso = os.path.join(self._box_folder, verso_name)
        if os.path.exists(dst_recto) | os.path.exists(dst_verso):
            raise GameError('there is already an img file for this card')
        shutil.copy(src_recto, dst_recto)
        shutil.copy(src_verso, dst_verso)

        card = dict(recto_path=dst_recto,
                    verso_path=dst_verso,
                    orientation=0,
                    card_name=card_name,
                    )
        self._box[card_name] = card
        self._varbox.save()

    def _check_card_in_game(self, card_name) -> dict:
        """look in deck or box if card present

        :card_name:
        :return: dict in which the card is contained or False if absent

        """
        for box_name, cards in self._all_cards.items():
            if card_name in cards:
                return cards
        return False

    def import_cards_folder(self, folder_path):
        """import all img file in the folder as cards. Every two file
        (in alhabetic order) will be the verso of the precedent card

        :folder_path: point to a folder of img file

        """
        filenames = os.listdir(folder_path)
        img_files = [
                fn for fn in filenames
                if filetype.is_image(os.path.join(folder_path, fn))]
        img_files.sort()
        cardlot_name = os.path.basename(folder_path)
        for recto, verso in zip(img_files[::2], img_files[1::2]):
            recto_path = os.path.join(folder_path, recto)
            verso_path = os.path.join(folder_path, verso)
            cardname = Path(recto_path).stem
            full_card_name = f'{cardlot_name}_{cardname}'
            self.import_card(recto_path, verso_path, full_card_name)

    def get_card(self, card_name: str) -> Card:
        """get any card present in the game

        :card_name: identify the card
        :returns: card to be displayed,

        """
        cards = self._check_card_in_game(card_name)
        if cards:
            card_dict = cards.get(card_name)
            card = Card(
                    **card_dict)
            return card
        else:
            raise GameError('missing from the game')

    def get_draw_pile_top_card(self) -> Card:
        """return the first card of the draw pile if any
        :returns:

        """
        if self.draw_pile_cards:
            obfuscated = self.draw_pile_cards[-1]
            card_name = self.get_real_card_name(obfuscated)
            card = self.get_card(card_name)
            return card
        else:
            return None

    def discover_card(self, card_name):
        """move a card from box to the deck (also the img file)

        :card_name:

        """
        if card_name in self.box_card_names:
            card = self._box.pop(card_name)
            src = card['recto_path']
            dst = self._deck_folder
            new_recto_path = shutil.move(src, dst)
            src = card['verso_path']
            new_verso_path = shutil.move(src, dst)
            card['recto_path'] = new_recto_path
            card['verso_path'] = new_verso_path
            card['pile'] = self._DISCARD_PILE
            self._deck[card_name] = card
            self._varbox.save()
        else:
            raise GameError(f'card {card_name} is not present in the box')

    def play_card(self, card_name):
        """put card in play pile

        :card_name:
        :returns:

        """
        pile = self.get_card_pile(card_name)
        if not pile == self._PERMANENT_PILE:
            if not pile == self._IN_PLAY_PILE:
                self._deck[card_name]['pile'] = self._IN_PLAY_PILE
                if pile == self._DRAW_PILE:
                    self._remove_from_draw(card_name)
                self._varbox.save()
            else:
                raise GameError('card is already in play')
        else:
            raise GameError(
                    'card cannot be play from permanent pile. '
                    'make it first non permanent')

    def play_first_card(self):
        """play the card that is on top of draw pile
        :returns:

        """
        pass

    def lock_card(self, card_name: str):
        """lock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card

        """
        pile = self.get_card_pile(card_name)
        if not pile == self._PERMANENT_PILE:
            self._deck[card_name]['pile'] = self._PERMANENT_PILE
            if pile == self._DRAW_PILE:
                self._remove_from_draw(card_name)
            self._varbox.save()
        else:
            raise GameError(
                    'card is already in permanent pile.')

    def unlock_card(self, card_name: str):
        """unlock a card, make it no longer permanent. Will part of the next
        shuffle

        :card_name: identify card

        """

        pile = self.get_card_pile(card_name)
        if pile == self._PERMANENT_PILE:
            self._deck[card_name]['pile'] = self._DISCARD_PILE
            self._varbox.save()
        else:
            raise GameError(
                    'card is not in permanent pile.')

    def discard(self, card_name):
        """move card in the discard pile

        :card_name:

        """
        pile = self.get_card_pile(card_name)
        if not pile == self._PERMANENT_PILE:
            if not pile == self._DISCARD_PILE:
                self._deck[card_name]['pile'] = self._DISCARD_PILE
                if pile == self._DRAW_PILE:
                    self._remove_from_draw(card_name)
                self._varbox.save()
            else:
                raise GameError('card is already discarded')
        else:
            raise GameError(
                    'permanent card cannot be discarded.')

    def _get_obfuscated_name(self, card_name):
        """

        :card_name: TODO
        :returns: TODO

        """
        if card_name not in self._draw_cards_obfuscate_name:
            card = self._deck.get(card_name)
            if not card.get(self._ALWAYS_VISIBLE):
                obfuscated = len(self._draw_cards_obfuscate_name)
                while obfuscated in self._draw_cards_real_name:
                    obfuscated += 1
            else:
                obfuscated = card_name
            self._draw_cards_real_name[obfuscated] = card_name
            self._draw_cards_obfuscate_name[card_name] = obfuscated
            self._varbox.save()
        else:
            obfuscated = self._draw_cards_obfuscate_name[card_name]
        return obfuscated

    def set_always_visible(self, card_name):
        """the card will be identifiable inside the draw pile also

        :card_name:
        :returns:

        """

        cards = self._check_card_in_game(card_name)
        if cards:
            card = cards.get(card_name)
            if not card.get(self._ALWAYS_VISIBLE):
                card[self._ALWAYS_VISIBLE] = True
            else:
                raise GameError('card is already always visible')
        else:
            raise GameError('card not found')

    def remove_always_visible(self, card_name):
        """the card will not be identifiable in the draw pile

        :card_name:
        :returns:

        """
        cards = self._check_card_in_game(card_name)
        if cards:
            card = cards.get(card_name)
            if card.get(self._ALWAYS_VISIBLE):
                card[self._ALWAYS_VISIBLE] = False
            else:
                raise GameError('card is already not always visible')
        else:
            raise GameError('card not found')

    def _remove_from_draw(self, card_name):
        """ to be called when card is removed from draw pile

        :card_name:
        :returns:

        """
        obfuscated = self._get_obfuscated_name(card_name)
        self._draw_cards_obfuscate_name.pop(card_name)
        self._draw_cards_real_name.pop(obfuscated)
        self._draw_pile.remove(obfuscated)
        self._varbox.save()

    def put_card_in_draw_pile(self, card_name, top=True):
        """move card in the draw pile

        :card_name:
        :top: put card on top of the pile. bottom if false

        """
        pile = self.get_card_pile(card_name)
        if not pile == self._PERMANENT_PILE:
            self._deck[card_name]['pile'] = self._DRAW_PILE
            obfuscated = self._get_obfuscated_name(card_name)
            if top:
                self._draw_pile.append(obfuscated)
            else:
                self._draw_pile.insert(0, obfuscated)
            self._varbox.save()
        else:
            raise GameError(
                    'permanent card cannot be in draw pile.')

    def shuffle_draw_pile(self):
        """shuffle cards in the draw pile

        """
        random.shuffle(self._draw_pile)

    def discard_all_cards_in_play(self):
        """

        """
        for card_name in self.in_play_cards:
            self.discard(card_name)

    def shuffle_back_all_discarded(self):
        """put all card from discarded pile into draw pile and shuffle
        :returns: TODO

        """
        for card_name in self.discarded_cards:
            self.put_card_in_draw_pile(card_name)
        self.shuffle_draw_pile()

    def forget_card(self, card_name):
        """move a card from deck to box

        :card_name:

        """
        if card_name in self.deck_card_names:
            pile = self.get_card_pile(card_name)
            if pile == self._DRAW_PILE:
                self._remove_from_draw(card_name)
            card = self._deck.pop(card_name)
            src = card['recto_path']
            dst = self._box_folder
            new_recto_path = shutil.move(src, dst)
            src = card['verso_path']
            new_verso_path = shutil.move(src, dst)
            card['recto_path'] = new_recto_path
            card['verso_path'] = new_verso_path
            card['orientation'] = 0
            self._box[card_name] = card
            self._varbox.save()
        else:
            raise GameError(f'card {card_name} is not present in the deck')

    def destroy_card(self, card_name):
        """remove card from deck or box and rm img file

        :card_name:

        """
        cards = self._check_card_in_game(card_name)
        if cards:
            card = cards.pop(card_name)
            pile = card.get('pile')
            if pile == self._DRAW_PILE:
                self._remove_from_draw(card_name)
            path = card['recto_path']
            os.remove(path)
            path = card['verso_path']
            os.remove(path)
            self._varbox.save()
        else:
            raise GameError('card is neither in deck, nor in box')

    def rotate_card(self, card_name):
        """rotate card  by 180 deg(progress)

        :card_name: identify the card
        """

        cards = self._check_card_in_game(card_name)
        if not cards:
            raise GameError('card not found')
        card_dict: dict = cards[card_name]
        orientation = card_dict['orientation']
        new_orientation = 2 * (orientation // 2) + (orientation + 1) % 2
        card_dict['orientation'] = new_orientation
        self._varbox.save()

    def flip_card(self, card_name):
        """flip recto-verso the card

        :card_name: identify the card
        """

        cards = self._check_card_in_game(card_name)
        if not cards:
            raise GameError('card not found')
        card_dict: dict = cards[card_name]
        orientation = card_dict['orientation']
        new_orientation = 3 - orientation
        card_dict['orientation'] = new_orientation
        self._varbox.save()


if __name__ == '__main__':
    pass
