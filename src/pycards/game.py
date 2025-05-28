import os
import shutil


import filetype


from pycards.config import DATA_FOLDER


SAVED_GAME_FILE_SUFFIX = 'json'
BOX_FOLDER = 'box'
DECK_FOLDER = 'deck'


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
        return self._box_card_names

    @property
    def deck_card_names(self) -> list:
        """return an ordered list of the card names in the deck"""
        return self.deck_card_names

    def __init__(self, name: str):
        self._name = name

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
        "TODO: check new name"

        if not filetype.is_image(recto_path):
            raise GameError('recto file is not an image')
        if not filetype.is_image(verso_path):
            raise GameError('recto file is not an image')

        filename, ext = os.path.splitext(recto_path)
        if card_name is None:
            card_name = os.path.basename(filename)
        folder = os.path.join(DATA_FOLDER, self.name, BOX_FOLDER)
        os.makedirs(folder, exist_ok=True)
        recto_name = f'{card_name}_recto{ext}'
        verso_name = f'{card_name}_verso{ext}'
        src_recto = recto_path
        dst_recto = os.path.join(folder, recto_name)
        src_verso = verso_path
        dst_verso = os.path.join(folder, verso_name)
        if os.path.exists(dst_recto) | os.path.exists(dst_verso):
            raise GameError('there is already an img file for this card')
        shutil.copy(src_recto, dst_recto)
        shutil.copy(src_verso, dst_verso)

    def import_cards_folder(self, folder_path):
        """import all img file in the folder as cards. Every two file
        (in alhabetic order) will be the verso of the precedent card

        :folder_path: point to a folder of img file

        """
        pass

    def get_card(self, card_name: str) -> Card:
        """get any card present in the game

        :card_name: identify the card
        :returns: card to be displayed,

        """
        pass

    def shuffle_deck(self) -> [Card]:
        """shuffle cards from deck
        :returns: list of all non-permanent cards
        in the deck in random order

        """
        pass

    def get_permanent_cards(self) -> [Card]:
        """get a list of permanent cards from the deck

        :returns: list of permanent cards

        """
        pass

    def discover_card(self, card_name):
        """move a card from box to the deck (also the img file)

        :card_name:

        """
        pass

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

    def lock_card(self, card_name: str):
        """lock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card

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

    def __init__(self, name: str, path_recto: str, path_verso: str, orientation: int):
        """create a card obj and get img_file to use and rotation 

        :name: identy card
        :path_recto: path to recto img
        :path_verso: path to verso img
        :orientation: 0(top recto), 1(down recto), 2(down verso), or 3(top verso)

        """
        self._name = name


if __name__ == '__main__':
    pass
