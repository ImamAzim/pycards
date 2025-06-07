from pycards.interfaces import GUI, BaseTable
import tkinter


class TkinterGUI(GUI, tkinter.Tk):

    """tkinter GUI for a pycards game"""

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('pycards')
        self._table = None
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self._menu_width = int(width * 1 / 5)
        self._table_width = int(width * 4 / 5)
        self.geometry("%dx%d" % (width, height))
        self._window_width = width
        self._window_height = height

        self._menu_frame = tkinter.LabelFrame(self, text='menu')
        self._cardlist_frame = tkinter.LabelFrame(self, text='cards')
        self._inspect_frame = tkinter.LabelFrame(self, text='inspector')
        self._table_frame = tkinter.LabelFrame(self, text='table')

        self._fill_menu()
        self._fill_cardlist()
        self._fill_inspect_frame()
        self._fill_table_frame()

        self._place_all_frames()

    def _place_all_frames(self):
        """position all frames in root window

        """
        self._menu_frame.grid(row=0, column=0)
        self._cardlist_frame.grid(row=1, column=0)
        self._inspect_frame.grid(row=2, column=0, columnspan=2)
        self._table_frame.grid(row=0, column=1, rowspan=4, columnspan=4)

    def _fill_menu(self):
        """put option in menu

        """
        button = tkinter.Button(
                self._menu_frame,
                text='quit',
                command=self.destroy,
                )
        button.pack()

    def _fill_cardlist(self):
        """list of box and deck cards, options with cards

        """
        pass

    def _fill_inspect_frame(self):
        """canvas and options

        """
        canvas = tkinter.Canvas(
                self._inspect_frame,
                bg='green',
                width=self._menu_width,
                height=self._window_height/2,
                )
        canvas.pack()
        button = tkinter.Button(
                self._inspect_frame,
                text='quit',
                command=self.destroy,
                )
        button.pack()

    def _fill_table_frame(self):
        """ prepare table where cards will be put

        """
        canvas = tkinter.Canvas(
                self._table_frame,
                bg='green',
                width=self._table_width,
                height=self._window_height,
                )
        canvas.pack()

    def set_table(self, table: BaseTable):
        self._table = table

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
