from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Literal


class BaseCard(metaclass=ABCMeta):

    """card object for a given orientation"""

    @abstractproperty
    def name(self) -> str:
        """card name"""
        pass

    @abstractproperty
    def path(self) -> str:
        """path to img file"""
        pass

    @abstractproperty
    def rotate(self) -> bool:
        """specify if img need to be rotated by 180 deg"""
        pass

    @abstractmethod
    def __init__(
            self,
            card_name: str,
            recto_path: str,
            verso_path: str,
            orientation: int,
            **others,
            ):
        """create a card obj and get img_file to use and rotation

        :card_name: identy card
        :recto_path: path to recto img
        :verso_path: path to verso img
        :orientation: 0(top recto), 1(down recto), 2(down verso), or
        3(top verso)

        """
        pass


class GUI(metaclass=ABCMeta):

    """GUI interface for a pycards game"""

    @abstractmethod
    def __init__(self):
        """gui interface for pycard game. a controller must be set after init
        :table: controller of the app"""
        pass

    @abstractmethod
    def run(self):
        """start the gui (in a loop)

        :returns: TODO

        """
        pass

    @abstractmethod
    def set_table(self, table):
        """set the controller of the view

        :table: controller of pycards

        """
        pass

    @abstractmethod
    def showinfo(self, msg: str):
        """display a msg, for example from controller

        :msg: message from controller

        """
        pass

    @abstractmethod
    def showerror(self, msg: str):
        """display an error msg, for example from controller

        :msg: message from controller

        """
        pass

    @abstractmethod
    def is_card_on_table(self, card_name) -> bool:
        """verify is card is present on the table (permanent or game zone)

        :card_name:
        :returns:

        """
        pass

    @abstractmethod
    def place_card_on_table(
            self,
            card_name: str,
            img_path: str,
            pile: Literal['game_zone', 'permanent'] = 'game_zone',
            rotated: bool = False):
        """place the card on the table. if card is already present it will only
        move it without updating
        the image

        :card_name: from file name withou recto or verso
        :img_path: path to card image
        :is_locked: for permanent card
        :pile: one of 'game_zone', 'permanent'
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    @abstractmethod
    def inspect_card(self,
                     card_name, str,
                     img_path: str,
                     rotated: bool = False,):
        """display card in larger frame and allow operations on it

        :card_name: from file name withou recto or verso
        :img_path: path to card image
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    @abstractmethod
    def clean_inspect_area(self):
        """remove the image from the inspect area and deactivate operations
        in it
        :returns: TODO

        """
        pass

    @abstractmethod
    def update_title(
            self, name: str):
        """update title
        :name: of the game
        """
        pass

    @abstractmethod
    def clean_table(self):
        """remove all cards from the table
        :returns: TODO

        """
        pass

    @abstractmethod
    def update_card_image(
            self,
            card_name: str,
            img_path: str,
            rotated: bool = False):
        """update a single card, for example when image is rotated

        :card_name: identify card
        :img_path: path to card image
        :rotated: True if you want to rotate by 108 deg

        """
        pass

    @abstractmethod
    def remove_card(self, card_name: str):
        """remove card from table, because destroyed, forgotten, or discarded

        :card_name: identify the card
        :returns:

        """
        pass

    @abstractmethod
    def update_draw_pile(
            self,
            draw_pile: list[str],
            card: BaseCard | None,
            ):
        """update the draw pile. names are usually obfuscated

        :draw_pile:
        :card:
        :returns:

        """
        pass

    @abstractmethod
    def update_discarded_pile(self, discarded: list[str]):
        """update the discarded pile

        :draw_pile:
        :returns:

        """
        pass

    @abstractmethod
    def update_box_cards_list(self, card_names: list[str]):
        """update the gui to show available cards in box

        :card_names:
        :returns:

        """
        pass


class BaseTable(object, metaclass=ABCMeta):

    """Table class to create and load games"""

    @abstractmethod
    def __init__(self, gui):
        """TODO: Docstring for __init__.

        """
        pass

    @abstractmethod
    def get_saved_games(self) -> [str]:
        """get a list of saved games on disk"""
        pass

    @abstractmethod
    def get_current_game(self) -> [str]:
        """return the name of the active game"""
        pass

    @abstractmethod
    def new_game(self, name: str):
        """create a new game and update gui with it

        :name: instance will be saved with this name
        """
        pass

    @abstractmethod
    def delete_game(self, name: str):
        """delete img and saved config files of game

        :name:
        """
        pass

    @abstractmethod
    def load_game(self, name: str):
        """make a game that was previousely saved active
        on the table

        :name: name of the game under it was saved
        """
        pass

    @abstractmethod
    def import_cards(self, folder_path: str):
        """import ('buy') cards. folder needs to contain for each card 2 img
        files

        :folder_path: contains the img file of the cards

        """
        pass

    @abstractmethod
    def discover_card(self, card_name: str):
        """move the cards from box to deck

        :card_name:
        :returns:

        """
        pass

    @abstractmethod
    def destroy_card(self, card_name: str):
        """remove from box or deck and rm img file

        :card_name: identify card
        :returns:

        """
        pass

    @abstractmethod
    def rotate_card(self, card_name):
        """rotate card

        :card_name: identify the card
        """
        pass

    @abstractmethod
    def flip(self, card_name):
        """flip card

        :card_name: identify the card
        """
        pass

    @abstractmethod
    def forget_card(self, card_name: str):
        """put back the card in box

        :card_name: identify the card
        :returns: TODO

        """
        pass

    @abstractmethod
    def lock_card(self, card_name: str):
        """lock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card
        :returns: TODO

        """
        pass

    @abstractmethod
    def unlock_card(self, card_name: str):
        """unlock a card, make it permanent. Will not be reshuffled in deck

        :card_name: identify card
        :returns: TODO

        """
        pass

    @abstractmethod
    def play_card(self, card_name: str):
        """put card in the in_play pile

        :card_name: identify card
        :returns:

        """
        pass

    @abstractmethod
    def discard(self, card_name: str):
        """put card in the discard pile

        :card_name: identify card
        :returns:

        """
        pass

    @abstractmethod
    def mark_card(self, card_name: str):
        """ mark card so that it will be visible in the draw pile

        :card_name: identify card
        :returns:

        """
        pass

    @abstractmethod
    def unmark_card(self, card_name: str):
        """ remove mark that it will not be visible in the draw pile

        :card_name: identify card
        :returns:

        """
        pass

    @abstractmethod
    def put_card_in_draw_pile(self, card_name: str):
        """

        :card_name: identify card
        :returns:

        """
        pass

    @abstractmethod
    def discard_all(self):
        """discard all cards from play zone
        :returns: TODO

        """
        pass

    @abstractmethod
    def shuffle_back(self):
        """put back all cards from discard in draw pile and shuffle
        :returns: TODO

        """
        pass

    @abstractmethod
    def inspect_card(self, card_name: str):
        """call inspect method of gui with card info to display

        :card_name:

        """
        pass

    @abstractmethod
    def draw_card(self):
        """play the first card from the draw pile
        :returns: TODO

        """
        pass
