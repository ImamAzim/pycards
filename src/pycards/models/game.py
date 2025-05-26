class Game(object):

    """Game class to handle the deck and the cards box"""

    @property
    def name(self) -> str:
        """doc"""
        return self._name

    def __init__(self, name: str):
        """TODO: to be defined. """
        self._name = name

    def function(self, arg1):
        """TODO: Docstring for function.

        :arg1: TODO
        :returns: TODO

        """
        self._arg = arg1


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
        pass


if __name__ == '__main__':
    pass
