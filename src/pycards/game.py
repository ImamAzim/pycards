import os
import shutil
from pathlib import Path
import random


import filetype


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
    def box_card_names(self) -> tuple:
        """return an ordered list of the card names in the box"""
        return tuple(sorted(self._box.keys()))

    @property
    def deck_card_names(self) -> tuple:
        """return an ordered list of the card names in the deck"""
        return tuple(sorted(self._deck.keys()))

    @property
    def permanent_cards(self) -> (Card):
        """get a list of permanent cards from the deck"""
        permanent_cards = [
                self.get_card(card_name)
                for card_name in self._permanent_cards]
        return tuple(permanent_cards)

    def __init__(self, name: str):
        self._name = name
        self._box = dict()
        self._deck = dict()
        self._all_cards = dict(box=self._box, deck=self._deck)
        self._permanent_cards = list()
        self._box_folder = os.path.join(DATA_FOLDER, self.name, BOX_FOLDER)
        os.makedirs(self._box_folder, exist_ok=True)
        self._deck_folder = os.path.join(DATA_FOLDER, self.name, DECK_FOLDER)
        os.makedirs(self._deck_folder, exist_ok=True)

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

    def _check_card_in_game(self, card_name):
        """look in deck or box if card present

        :card_name:

        """
        for box_name, cards in self._all_cards.items():
            if card_name in cards:
                return True
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
        if self._check_card_in_game(card_name):
            for box_name, cards in self._all_cards.items():
                card_dict = cards.get(card_name)
                if card_dict is not None:
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
        else:
            raise GameError('card is not present in the box')

    def lock_card(self, card_name: str):
        """lock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card

        """
        if card_name in self.deck_card_names:
            if card_name not in self._permanent_cards:
                self._permanent_cards.append(card_name)
            else:
                raise GameError('card is already marked as permanent')
        else:
            raise GameError('card is not present in the deck')

    def unlock_card(self, card_name: str):
        """unlock a card, make it no longer permanent. Will part of the next
        shuffle

        :card_name: identify card

        """
        if card_name in self._permanent_cards:
            self._permanent_cards.remove(card_name)
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
        pass

    def destroy_card(self, card_name):
        """remove card from deck or box and rm img file

        :card_name:

        """
        pass

    def rotate_card(self, card_name, direction: str = 'right'):
        """flip or rotate card (progress)

        :card_name: identify the card
        :direction: either right or down
        """
        pass


class GameHandler(object):

    """class to create, load or save games"""

    @property
    def game(self) -> None | Game:
        """doc"""
        return self._game

    def __init__(self):
        """TODO: to be defined. """
        self._game = None

    def new_game(self, name: str):
        """create an instance of a new game and save it

        :name: identify name

        """
        self._game = Game(name)

    def load_game(self, name: str):
        """load game and put it in attribute

        :name: same str as it was saved

        """
        pass

    def delete_game(self, name: str):
        """remove game from disk

        :name: same as it was saved

        """
        savefile = f'{name}.{SAVED_GAME_FILE_SUFFIX}'
        filenames = os.listdir(DATA_FOLDER)
        if savefile in filenames:
            path = os.path.join(DATA_FOLDER, savefile)
            os.remove(path)
        if name in filenames:
            path = os.path.join(DATA_FOLDER, name)
            shutil.rmtree(path)


if __name__ == '__main__':
    pass
