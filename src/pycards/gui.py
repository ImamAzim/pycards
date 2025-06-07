from pycards.table import Table


class GUI():

    """GUI for a pycards game"""

    def __init__(self, table: Table):
        """gui interface for pycard game
        :table: controller of the app"""

        self._table = table

    def display_msg(self, msg: str):
        """display a msg, for example from controller

        :msg: message from controller

        """
        pass

    def place_card_on_table(
            self,
            card_name: str,
            img_path: str,
            is_locked: bool,
            pile: str = 'deck',
            rotated: bool = False):
        """place the card on the table. if card is already present it will only
        move it without updating
        the image

        :card_name: from file name withou recto or verso
        :img_path: path to card image
        :is_locked: for permanent card
        :pile: one of 'deck', 'discard' or 'gamezone'
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    def inspect_card(self,
                     card_name, str,
                     img_path: str,
                     is_locked: bool,
                     rotated: bool = False,):
        """display card in larger frame and allow operations on it

        :card_name: from file name withou recto or verso
        :img_path: path to card image
        :is_locked: for permanent card. should be visible in the gui
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    def clean_inspect_area(self):
        """remove the image from the inspect area and deactivate operations
        in it
        :returns: TODO

        """
        pass

    def is_card_on_table(self, card_name: str) -> bool:
        """check if the card is present on the table

        :card_name: identify card
        :returns: True if card is on table, else False

        """
        pass

    def update_title(
            self, name: str):
        """update title
        :name: of the game
        """
        pass

    def clean_table(self):
        """remove all cards from the table
        :returns: TODO

        """
        pass
        self.clean_inspect_area()

    def update_card_image(
            self,
            card_name: str,
            img_path: str,
            is_locked: bool,
            rotated: bool = False):
        """update a single card, for example when image is rotated

        :card_name: identify card
        :img_path: path to card image
        :is_locked: for permanent card. should be visible in the gui
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    def remove_card(self, card_name: str):
        """remove card from table, because destroyed or forgotten

        :card_name: identify the card
        :returns:

        """
        pass

    def update_box_cards_list(self, card_names: list[str]):
        """update the gui to show available cards in box

        :card_names:
        :returns:

        """
        pass

    def update_deck_cards_list(self, card_names: list[str]):
        """update the gui to show available cards in player's deck

        :card_names:
        :returns:

        """
        pass
