import os
import shutil


import filetype


from pycards.config import DATA_FOLDER


SAVED_GAME_FILE_SUFFIX = 'json'
BOX_FOLDER = 'box'
DECK_FOLDER = 'deck'


class GameError(Exception): pass


class Game(object):

    """Game class to handle the deck and the cards box"""

    @property
    def name(self) -> str:
        """doc"""
        return self._name

    def __init__(self, name: str):
        """TODO: to be defined. """
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
        "TODO: check file are images, new filename, new name"

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
        src = recto_path
        dst = os.path.join(folder, recto_name)
        shutil.copy(src, dst)
        src = verso_path
        dst = os.path.join(folder, verso_name)
        shutil.copy(src, dst)


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
