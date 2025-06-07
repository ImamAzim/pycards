from pycards.interfaces import GUI, BaseTable
import tkinter


class BaseGUI(GUI):

    """base GUI. incorporate basic callbacks that use controller. Can be base for any GUI,
    wether based on tkinter, pygames, etc... the method from GUI interface must be written
    in the children class"""

    def _new_game(self, name: str):
        """create a new game

        :name: TODO
        :returns: TODO

        """

    def set_table(self, table: BaseTable):
        self._table = table


class TkinterGUI(BaseGUI, tkinter.Tk):

    """tkinter GUI for a pycards game"""

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('pycards')
        self._table = None

    def run(self):
        self.mainloop()


    def display_msg(self, msg: str):
        pass

    def place_card_on_table(
            self,
            card_name: str,
            img_path: str,
            is_locked: bool,
            pile: str = 'deck',
            rotated: bool = False):
        pass

    def inspect_card(self,
                     card_name, str,
                     img_path: str,
                     is_locked: bool,
                     rotated: bool = False,):
        pass

    def clean_inspect_area(self):
        pass

    def is_card_on_table(self, card_name: str) -> bool:
        pass

    def update_title(
            self, name: str):
        pass

    def clean_table(self):
        pass
        self.clean_inspect_area()

    def update_card_image(
            self,
            card_name: str,
            img_path: str,
            is_locked: bool,
            rotated: bool = False):
        pass

    def remove_card(self, card_name: str):
        pass

    def update_box_cards_list(self, card_names: list[str]):
        pass

    def update_deck_cards_list(self, card_names: list[str]):
        pass


if __name__ == '__main__':
    gui = TkinterGUI()
    gui.run()
