from abc import ABC, abstractmethod


class GUI(ABC):

    """GUI for a pycards game"""

    def __init__(self):
        """TODO: to be defined. """
        ABC.__init__(self)

    @abstractmethod
    def add_card_on_table(self, card_name: str, img_path: str, pile: str, rotated=False: bool):
        """TODO: Docstring for add_card_on_table.

        :card_name: from file name withou recto or verso
        :img_path: path to card image
        :location: either 'deck' or 'discard'
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    @abstractmethod
    def update_title(self, name: str):
        """put the name of the game on title of table

        :name: of the game
        """
        pass

    @abstractmethod
    def update_card_image(self, card_name: str):
        """update a single card, for example when image is rotated

        :card_name: identify card, which should have a object in the GUI

        """
        pass

    @abstractmethod
    def update_box_cards_list(self, card_names: list[str]):
        """update the gui to show available cards in box

        :card_names:
        :returns:

        """
        pass

    @abstractmethod
    def update_deck_cards_list(self, card_names: list[str]):
        """update the gui to show available cards in player's deck

        :card_names:
        :returns:

        """
        pass


class TkinterGUI(GUI):

    """Docstring for TkinterGUI. """

    def __init__(self):
        """TODO: to be defined. """
        GUI.__init__(self)

