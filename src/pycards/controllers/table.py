from pycards.models import Game


class Table(object):

    """Table class to create and load games"""

    @property
    def game(self) -> Game | None:
        """active game on table"""
        return self._game

    @game.setter
    def game(self, value: Game | None):
        self._game = value

    def __init__(self):
        """TODO: Docstring for __init__.

        """
        self.game = None

    def new_game(self, name: str):
        """create an instance of a game, activate it on the table and save it

        :name: instance will be saved with this name
        """
        pass

    def load_game(self, name: str):
        """make a game that was previousely saved active
        on the table

        :name: name of the game under it was saved
        """
        pass


if __name__ == '__main__':
    pass
