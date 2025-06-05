import os
import shutil
from pathlib import Path
import random


import filetype
from varboxes import VarBox


from pycards.config import DATA_FOLDER


SAVED_GAME_FILE_SUFFIX = 'json'
BOX_FOLDER = 'box'
DECK_FOLDER = 'deck'


class Card(object):

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
    def permanent_cards(self) -> (Card):
        """get a list of permanent cards from the deck"""
        permanent_cards = [
                self.get_card(card_name)
                for card_name in self._permanent_cards]
        return tuple(permanent_cards)

    def __init__(self, name: str):
        self._change_name(name)

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
        self._all_cards = dict(box=self._box, deck=self._deck)
        self._permanent_cards = self._varbox.permanent_cards

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
        if not hasattr(varbox, 'permanent_cards'):
            varbox.permanent_cards = list()
        return varbox

    def _reset_varbox(self):
        """reset all the data of the current varbox

        """
        varbox = self._varbox
        varbox.box = dict()
        varbox.deck = dict()
        varbox.permanent_cards = list()

    def is_card_permanent(self, card_name) -> bool:
        """determine if card is in the list of permanent cards

        :card_name:
        :returns: True if in list of permanents

        """
        if card_name in self._permanent_cards:
            return True
        else:
            return False

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
        return varbox_path

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
            card = Card(**card_dict)
            return card
        else:
            raise GameError('missing from the game')

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
            self._deck[card_name] = card
            self._varbox.save()
        else:
            raise GameError('card is not present in the box')

    def lock_card(self, card_name: str):
        """lock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card

        """
        if card_name in self.deck_card_names:
            if not self.is_card_permanent(card_name):
                self._permanent_cards.append(card_name)
                self._varbox.save()
            else:
                raise GameError('card is already marked as permanent')
        else:
            raise GameError('card is not present in the deck')

    def unlock_card(self, card_name: str):
        """unlock a card, make it no longer permanent. Will part of the next
        shuffle

        :card_name: identify card

        """
        if self.is_card_permanent(card_name):
            self._permanent_cards.remove(card_name)
            self._varbox.save()
        else:
            raise GameError('card is already not marked as non-permanent')

    def shuffle_deck(self) -> [Card]:
        """shuffle cards from deck
        :returns: tuple of all non-permanent cards
        in the deck in random order

        """
        pile = [
                Card(**self._deck[card_name])
                for card_name in self.deck_card_names
                if card_name not in self._permanent_cards]
        random.shuffle(pile)
        return pile

    def forget_card(self, card_name):
        """move a card from deck to box

        :card_name:

        """
        if card_name in self.deck_card_names:
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
            raise GameError('card is not present in the deck')

    def destroy_card(self, card_name):
        """remove card from deck or box and rm img file

        :card_name:

        """
        cards = self._check_card_in_game(card_name)
        if cards:
            if self.is_card_permanent(card_name):
                self.unlock_card(card_name)
            card = cards.pop(card_name)
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
        card_dict: dict = cards[card_name]
        orientation = card_dict['orientation']
        new_orientation = 3 - orientation
        card_dict['orientation'] = new_orientation
        self._varbox.save()


if __name__ == '__main__':
    pass
