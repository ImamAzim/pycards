from pycards.interfaces import GUI, BaseTable
import tkinter
from tkinter import ttk


class TkinterGUI(GUI, tkinter.Tk):

    """tkinter GUI for a pycards game"""
    TABLE_WIDTH_WEIGHT = 4

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('pycards')
        self._table = None
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self._table_width = int(
                width * self.TABLE_WIDTH_WEIGHT / (self.TABLE_WIDTH_WEIGHT + 1)
                )
        geometry = f'{width}x{height}'
        self.geometry(geometry)
        self._width = width
        self._height = height

        self._menu_frame = ttk.LabelFrame(self, text='menu')
        self._cardlist_frame = ttk.LabelFrame(self, text='cards')
        self._inspect_frame = ttk.LabelFrame(self, text='inspector')
        self._table_frame = ttk.LabelFrame(self, text='table')

        self._fill_menu()
        self._fill_cardlist()
        self._fill_inspect_frame()
        self._fill_table_frame()

        self._place_all_frames()

    def _place_all_frames(self):
        """position all frames in root window

        """
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=self.TABLE_WIDTH_WEIGHT)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self._menu_frame.grid(row=0, column=0, sticky=tkinter.EW)
        self._cardlist_frame.grid(row=1, column=0, sticky=tkinter.EW)
        self._inspect_frame.grid(row=2, column=0, sticky=tkinter.EW)
        self._table_frame.grid(row=0, column=1, rowspan=3, sticky=tkinter.NSEW)

    def _fill_menu(self):
        """put option in menu

        """
        button = ttk.Button(
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
        pass
        # canvas = tkinter.Canvas(
                # self._inspect_frame,
                # bg='green',
                # # width=self._menu_width,
                # # height=self._window_height/2,
                # )
        # canvas.pack()
        # button = ttk.Button(
                # self._inspect_frame,
                # text='quit',
                # command=self.destroy,
                # )
        # button.pack()

    def _fill_table_frame(self):
        """ prepare table where cards will be put

        """
        canvas = tkinter.Canvas(
                self._table_frame,
                bg='green',
                height=self._height,
                # width=self._width,
                scrollregion=(0, 0, self._width, 3 * self._height),
                )
        vbar = ttk.Scrollbar(self._table_frame, orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        print(canvas['width'])
        print(canvas['height'])

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
