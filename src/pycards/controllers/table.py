from pycards.models import Game
from pycards.views import GUI


class Table(object):

    """Table class to create and load games"""

    @property
    def game(self) -> Game | None:
        """active game on table"""
        return self._game

    @game.setter
    def game(self, value: Game | None):
        self._game = value

    def __init__(self, gui: GUI):
        """TODO: Docstring for __init__.

        """

        self._gui = gui
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

    def import_cards(self, folder_path: str):
        """import or buy cards. folder needs to contain for each card 2 img files, with names XXX_recto.jpg
        and XXX_verso.jpg

        :folder_path: contains the img file of the cards

        """
        pass

    def discover_card(self, card_name: str):
        """move the cards from box to deck

        :card_name:
        :returns:

        """
        pass

    def destroy_card(self, card_name: str):
        """remove from box or deck and rm img file

        :card_name: identify card
        :returns:

        """
        pass

    def rotate_card(self, direction: str = 'right'):
        """flip or rotate card (progress)

        :direction: either right or down
        """
        pass

    def forget_card(self, card_name: str):
        """put back the card in box

        :card_name: identify the card
        :returns: TODO

        """
        pass


if __name__ == '__main__':
    pass
