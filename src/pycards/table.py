from pycards.game import Game, GameError
from pycards.interfaces import GUI


class Table(object):

    """Table class to create and load games"""

    def __init__(self, gui: GUI):
        """TODO: Docstring for __init__.

        """

        self._gui = gui
        self._game = Game()

    def new_game(self, name: str):
        """create a new game and update gui with it

        :name: instance will be saved with this name
        """
        try:
            self._game.new(name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            self._gui.clean_table()
            name = self._game.name
            self._gui.update_title(name)
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            deck_cards_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_cards_names)

    def load_game(self, name: str):
        """make a game that was previousely saved active
        on the table

        :name: name of the game under it was saved
        """
        try:
            self._game.load(name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            self._gui.clean_table()
            name = self._game.name
            self._gui.update_title(name)
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            deck_cards_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_cards_names)
            self.shuffle_deck()

    def import_cards(self, folder_path: str):
        """import ('buy') cards. folder needs to contain for each card 2 img
        files

        :folder_path: contains the img file of the cards

        """
        try:
            self._game.import_cards_folder(folder_path)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)

    def discover_card(self, card_name: str):
        """move the cards from box to deck

        :card_name:
        :returns:

        """
        try:
            self._game.discover_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            deck_card_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_card_names)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    'discard',
                    card.rotate)
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    card.rotate)

    def destroy_card(self, card_name: str):
        """remove from box or deck and rm img file

        :card_name: identify card
        :returns:

        """
        try:
            self._game.destroy_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            deck_card_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_card_names)
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)
            self._gui.clean_inspect_area()

    def rotate_card(self, card_name):
        """rotate card

        :card_name: identify the card
        """
        try:
            self._game.rotate_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            card = self._game.get_card(card_name)
            if self._gui.is_card_on_table(card_name):
                self._gui.update_card_image(
                        card_name,
                        card.path,
                        self._game.is_card_permanent(card_name),
                        card.rotate,
                        )
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    card.rotate)

    def flip(self, card_name):
        """flip card

        :card_name: identify the card
        """
        try:
            self._game.flip_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            card = self._game.get_card(card_name)
            if self._gui.is_card_on_table(card_name):
                self._gui.update_card_image(
                        card_name,
                        card.path,
                        self._game.is_card_permanent(card_name),
                        card.rotate,
                        )
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    card.rotate)

    def forget_card(self, card_name: str):
        """put back the card in box

        :card_name: identify the card
        :returns: TODO

        """
        try:
            self._game.forget_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            deck_card_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_card_names)
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)
            self._gui.clean_inspect_area()

    def lock_card(self, card_name: str):
        """lock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card
        :returns: TODO

        """
        try:
            self._game.lock_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            card = self._game.get_card(card_name)
            if self._gui.is_card_on_table(card_name):
                self._gui.update_card_image(
                        card_name,
                        card.path,
                        self._game.is_card_permanent(card_name),
                        card.rotate,
                        )
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    card.rotate)

    def unlock_card(self, card_name: str):
        """unlock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card
        :returns: TODO

        """
        try:
            self._game.unlock_card(card_name)
        except GameError as e:
            self._gui.display_msg(e)
        else:
            card = self._game.get_card(card_name)
            if self._gui.is_card_on_table(card_name):
                self._gui.update_card_image(
                        card_name,
                        card.path,
                        self._game.is_card_permanent(card_name),
                        card.rotate,
                        )
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    card.rotate)

    def inspect_card(self, card_name: str):
        """call inspect method of gui with card info to display

        :card_name:

        """
        card = self._game.get_card(card_name)
        self._gui.inspect_card(
                card_name,
                card.path,
                self._game.is_card_permanent(card_name),
                card.rotate)

    def shuffle_deck(self):
        """shuffle the cards that are not permanent and place them in the deck
        :returns: TODO

        """
        cards = self._game.shuffle_deck()
        for card in cards:
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    'deck',
                    card.rotate)
        permanent_cards = self._game.permanent_cards()
        for card in permanent_cards:
            if not self._gui.is_card_on_table(card.name):
                self._gui.place_card_on_table(
                        card.name,
                        card.path,
                        True,
                        'gamezone',
                        card.rotate)
        self._gui.clean_inspect_area()


if __name__ == '__main__':
    pass
