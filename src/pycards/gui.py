from pycards.interfaces import GUI, BaseTable
import tkinter
from tkinter import ttk


class TkinterGUI(GUI, tkinter.Tk):

    """tkinter GUI for a pycards game"""
    TABLE_WIDTH_WEIGHT = 4  # relative wieght to menu column
    TABLE_REL_HEIGHT = 3  # unit of screen height

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('pycards')
        self._table = None
        self._table_frame: tkinter.Frame
        self._cardlist_frame: tkinter.Frame
        self._inspect_frame: tkinter.Frame

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self._table_width = int(
                width * self.TABLE_WIDTH_WEIGHT / (self.TABLE_WIDTH_WEIGHT + 1)
                )
        self._table_height = self.TABLE_REL_HEIGHT * height
        self._menu_width = width / (self.TABLE_WIDTH_WEIGHT + 1)
        geometry = f'{width}x{height}'
        self.geometry(geometry)
        self._width = width
        self._height = height
        self._inspector_height = self._height / 2

        self._create_menu()
        self._create_cardlist_frame()
        self._create_inspect_frame()
        self._create_table_frame()

        self._place_all_frames()

        self.update()
        self._table_width = self._canvas_table.winfo_width()
        self._inspector_width = self._canvas_inspector.winfo_width()

    def _place_all_frames(self):
        """position all frames in root window

        """
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=self.TABLE_WIDTH_WEIGHT)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._cardlist_frame.grid(row=0, column=0, sticky=tkinter.EW)
        self._inspect_frame.grid(row=1, column=0, sticky=tkinter.NSEW)
        self._table_frame.grid(row=0, column=1, rowspan=2, sticky=tkinter.NSEW)

    def _create_menu(self):
        """put option in menu

        """
        menubar = tkinter.Menu(self)
        self.config(menu=menubar)
        file_menu = tkinter.Menu(menubar)
        file_menu.add_command(
                label='new game',
                command=self._prompt_new_game,
                )
        file_menu.add_command(
                label='load game',
                command=self._prompt_load_game,
                )
        file_menu.add_command(
                label='delete active game',
                command=self._prompt_delete,
                )
        file_menu.add_command(
                label='quit',
                command=self.destroy,
                )
        menubar.add_cascade(
                label='File',
                menu=file_menu,
                underline=0,
                )

    def _prompt_new_game(self):
        """ask for a new game name

        """
        pass

    def _prompt_load_game(self):
        """present games that can be loaded

        """
        pass

    def _prompt_delete(self):
        """ask if you are sure to delete this game

        """
        pass

    def _create_cardlist_frame(self):
        """list of box and deck cards, options with cards

        """
        self._cardlist_frame = ttk.LabelFrame(self, text='cards')
        ttk.Label(self._cardlist_frame, text='TODO: option menus for cards lists').pack(fill=tkinter.X)


    def _create_inspect_frame(self):
        """canvas and options

        """
        self._inspect_frame = ttk.LabelFrame(self, text='inspector')
        canvas = tkinter.Canvas(
                self._inspect_frame,
                bg='green',
                width=1,
                height=self._inspector_height,
                )
        canvas.pack(expand=True, fill=tkinter.X)
        self._canvas_inspector = canvas

    def _create_table_frame(self):
        """ prepare table where cards will be put

        """
        self._table_frame = ttk.LabelFrame(self, text='table')
        canvas = tkinter.Canvas(
                self._table_frame,
                bg='green',
                height=self._table_height,
                # width=self._table_width,
                scrollregion=(0, 0, self._width, 3 * self._height),
                )
        vbar = ttk.Scrollbar(self._table_frame, orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        self._canvas_table = canvas

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
