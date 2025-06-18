import tkinter
from tkinter import simpledialog, filedialog, messagebox
from tkinter import ttk


from PIL import Image, ImageTk, ImageFile


from pycards.interfaces import GUI, BaseTable, BaseCard


class LoadPrompt(simpledialog.Dialog):

    """prompt to show games that can be loaded. use a dropdown menu
    (combobox) """

    def __init__(self, parent, saved_games: [str]):
        self._saved_games = saved_games
        super().__init__(parent)

    def body(self, master):
        """
        """
        self._save_games_list = ttk.Combobox(
                master,
                state='readonly',
                values=self._saved_games,
                )
        self._save_games_list.set(self._saved_games[0])
        self._save_games_list.pack()
        self.game_name = False

    def apply(self):
        self.game_name = self._save_games_list.get()


class TkinterGUI(GUI, tkinter.Tk):

    """tkinter GUI for a pycards game"""
    TABLE_WIDTH_WEIGHT = 30  # relative wieght to menu column
    TABLE_REL_HEIGHT = 3  # unit of screen height
    _PERMANENT_ZONE_HEIGHT = 1 / 4 # of the screen height
    _TABLE_WIDTH_IN_CARDS = 6
    _IMG_KEY = 'img'
    _IMG_LABEL_KEY = 'img_label'

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('pycards')
        self._table = None
        self._game_name: str = None
        self._inspected_card = tkinter.StringVar(self)
        self._inspected_card.set(None)
        self._cards_on_table: dict[str, dict] = dict()
        self._table_frame: tkinter.Frame
        self._permanent_frame: tkinter.Frame
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
        self._create_permanent_frame()

        self._place_all_frames()

        self.update()
        self._table_width = self._canvas_table.winfo_width()
        self._inspector_width = self._canvas_inspector.winfo_width()

    def _place_all_frames(self):
        """position all frames in root window

        """
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=self.TABLE_WIDTH_WEIGHT)
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        self._cardlist_frame.grid(row=0, column=0, sticky=tkinter.EW)
        self._inspect_frame.grid(row=1, column=0, sticky=tkinter.NSEW)
        self._permanent_frame.grid(
                row=0, column=1, sticky=tkinter.NSEW)
        self._table_frame.grid(
                row=1, column=1, sticky=tkinter.NSEW)

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
                label='import cards',
                command=self._prompt_import,
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
        game_name = simpledialog.askstring(
                'new game', 'enter the name of your game:')
        if game_name:
            self._table.new_game(game_name)

    def _prompt_import(self):
        """ask for a folder to import

        """
        path = filedialog.askdirectory(title='select a folder with cards')
        if path:
            self._table.import_cards(path)

    def _prompt_load_game(self):
        """present games that can be loaded

        """
        games = self._table.get_saved_games()
        prompt = LoadPrompt(self, games)
        game = prompt.game_name
        if game:
            self._table.load_game(game)

    def _prompt_delete(self):
        """ask if you are sure to delete this game

        """
        gamename = self._table.get_current_game()
        message = (
                'are you sure you want to delete '
                f'the current game ({gamename})'
                )
        answer = messagebox.askyesno(
                title='delete',
                message=message,
                )
        if answer:
            self._table.delete_game()

    def _create_cardlist_frame(self):
        """list of box and deck cards, options with cards

        """
        self._cardlist_frame = ttk.LabelFrame(self, text='cards')

        box_cards_frame = ttk.LabelFrame(
                self._cardlist_frame,
                text='box cards',
                )
        box_cards_frame.pack(fill=tkinter.X)
        self._boxcards_list = ttk.Combobox(
                box_cards_frame,
                state='readonly'
                )
        self._boxcards_list.pack(
                side=tkinter.LEFT,
                expand=True,
                fill=tkinter.X,
                )
        ttk.Button(
                box_cards_frame,
                text='<-inspect...',
                command=lambda: self._table.inspect_card(
                    self._boxcards_list.get()),
                ).pack(side=tkinter.LEFT)

        drawpile_frame = ttk.LabelFrame(
                self._cardlist_frame,
                text='draw pile',
                )
        drawpile_frame.pack(fill=tkinter.X)
        self._drawpile = ttk.Combobox(
                drawpile_frame,
                state='readonly',
                )
        self._drawpile.grid(
                column=0,
                row=0,)
        ttk.Button(
                drawpile_frame,
                text='draw...',
                command=lambda: self._table.draw_card(),
                ).grid(column=0, row=2, sticky=tkinter.EW)
        ttk.Button(
                drawpile_frame,
                text='inspect...',
                command=lambda: self._table.inspect_obfuscated_card(
                    self._drawpile.get()),
                ).grid(column=0, row=1, stick=tkinter.EW)
        self._top_card_label = tkinter.Label(
                drawpile_frame,
                )
        self._top_card_label.grid(column=1, row=0, rowspan=3)

        discardpile_frame = ttk.LabelFrame(
                self._cardlist_frame,
                text='discard pile',
                )
        discardpile_frame.pack(fill=tkinter.X)
        self._discardpile = ttk.Combobox(
                discardpile_frame,
                state='readonly',
                )
        self._discardpile.bind(
                '<<ComboboxSelected>>',
                lambda event: self._table.inspect_card(
                    self._discardpile.get()),
                )
        self._discardpile.pack(
                expand=True, fill=tkinter.X)

    def _call_discover(self):
        card_name = self._inspected_card.get()
        self._table.discover_card(card_name)

    def _create_inspect_frame(self):
        """canvas and options

        """
        self._inspect_frame = ttk.LabelFrame(self, text='inspector')
        canvas = tkinter.Canvas(
                self._inspect_frame,
                bg='green',
                width=self._menu_width,
                height=self._inspector_height,
                )
        canvas.pack(expand=False, fill=tkinter.X)
        buttons_frame = ttk.Frame(self._inspect_frame)
        buttons_frame.pack()
        ttk.Button(
                buttons_frame,
                text='discover',
                command=lambda: self._table.discover_card(
                    self._inspected_card.get()),
                ).grid(row=0, column=0)
        ttk.Button(
                buttons_frame,
                text='forget',
                command=lambda: self._table.forget_card(
                    self._inspected_card.get()),
                ).grid(row=0, column=1)
        ttk.Button(
                buttons_frame,
                text='destroy',
                command=lambda: self._table.destroy_card(
                    self._inspected_card.get()),
                ).grid(row=0, column=2)
        ttk.Button(
                buttons_frame,
                text='rotate',
                command=lambda: self._table.rotate_card(
                    self._inspected_card.get()),
                ).grid(row=1, column=0)
        ttk.Button(
                buttons_frame,
                text='flip',
                command=lambda: self._table.flip(
                    self._inspected_card.get()),
                ).grid(row=1, column=1)
        ttk.Button(
                buttons_frame,
                text='lock',
                command=lambda: self._table.lock_card(
                    self._inspected_card.get()),
                ).grid(row=1, column=2)
        ttk.Button(
                buttons_frame,
                text='unlock',
                command=lambda: self._table.unlock_card(
                    self._inspected_card.get()),
                ).grid(row=1, column=3)
        self._canvas_inspector = canvas

    def _create_table_frame(self):
        """ prepare table where cards will be put

        """
        self._table_frame = ttk.LabelFrame(self, text='game zone')
        canvas = tkinter.Canvas(
                self._table_frame,
                bg='green',
                height=self._height*(1-self._PERMANENT_ZONE_HEIGHT),
                # scrollregion=(0, 0, self._width, 3 * self._height),
                )
        vbar = ttk.Scrollbar(self._table_frame, orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        self._canvas_table = canvas

    def _create_permanent_frame(self):
        """prepare canvas where permanent cards are put
        :returns: TODO

        """
        self._permanent_frame = ttk.LabelFrame(self, text='permanent cards')
        canvas = tkinter.Canvas(
                self._permanent_frame,
                bg='blue',
                height=self._height*self._PERMANENT_ZONE_HEIGHT,
                scrollregion=(0, 0, self._width, self._height),
                )
        vbar = ttk.Scrollbar(self._permanent_frame, orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        self._canvas_permanent = canvas

    def showerror(self, msg: str):
        tkinter.messagebox.showerror(
                title='error',
                message=msg,
                )

    def showinfo(self, msg: str):
        tkinter.messagebox.showinfo(
                title='info',
                message=msg,
                )

    def set_table(self, table: BaseTable):
        self._table = table

    def run(self):
        self.mainloop()

    def place_card_on_table(
            self,
            card_name: str,
            img_path: str,
            is_locked: bool = False,
            pile: str = 'deck',
            rotated: bool = False):

        card_width = self._table_width / self._TABLE_WIDTH_IN_CARDS
        y = self._height / 2
        if pile == 'deck':
            x = 0
        elif pile == 'discard':
            x = self._table_width - card_width
        else:
            x = self._table_width / 2

        canvas = self._canvas_table
        if not self.is_card_on_table(card_name):
            self._cards_on_table[card_name] = dict()
            placed_card = self._cards_on_table[card_name]
            img: ImageFile.ImageFile = Image.open(img_path)
            maxsize = (card_width, self._table_height)
            img.thumbnail(maxsize)
            if rotated:
                img = img.rotate(180)
            placed_card[self._IMG_KEY] = ImageTk.PhotoImage(img)
            label = tkinter.Label(
                    canvas,
                    image=placed_card[self._IMG_KEY],
                    cursor='hand1',
                    )
            label.place(x=x, y=y, anchor=tkinter.NW)
            placed_card[self._IMG_LABEL_KEY] = label
            label.bind(
                    "<ButtonPress-1>",
                    lambda e: self._on_card_click(e, card_name))
            label.bind(
                    "<B1-Motion>",
                    lambda e: self._on_card_drop(e, card_name))
            if is_locked:
                label['background'] = 'blue'
            else:
                label['background'] = 'green'
        else:
            placed_card = self._cards_on_table[card_name]
            label = placed_card[self._IMG_LABEL_KEY]
            label.place(x=x, y=y, anchor=tkinter.NW)

    def _on_card_click(self, event: tkinter.Event, card_name: str):
        self._table.inspect_card(card_name)
        self._cursor_x0 = event.x
        self._cursor_y0 = event.y
        card_label: tkinter.Label = event.widget
        card_label.lift()

    def _on_card_drop(self, event: tkinter.Event, card_name: str):
        cursor_x = event.x
        cursor_y = event.y
        dx = cursor_x - self._cursor_x0
        dy = cursor_y - self._cursor_y0
        x = event.widget.winfo_x() + dx
        y = event.widget.winfo_y() + dy
        event.widget.place(x=x, y=y)

    def inspect_card(self,
                     card_name: str,
                     img_path: str,
                     is_locked: bool,
                     rotated: bool = False,):

        self._inspected_card.set(card_name)
        self._inspect_frame['text'] = f'inspect: {card_name}'

        canvas = self._canvas_inspector
        canvas.delete(tkinter.ALL)
        img: ImageFile.ImageFile = Image.open(img_path)
        maxsize = (self._inspector_width, self._inspector_height)
        img.thumbnail(maxsize)
        if rotated:
            img = img.rotate(180)
        canvas.img = ImageTk.PhotoImage(img)
        x = self._inspector_width / 2
        y = self._inspector_height / 2
        canvas.create_image(
                x, y,
                image=canvas.img,
                )
        if is_locked:
            w, h = img.size
            canvas.create_rectangle(
                    (x-w/2, y-h/2),
                    (x+w/2, y+h/2),
                    outline='blue',
                    width=2,
                    )

    def clean_inspect_area(self):
        self._inspected_card.set(None)
        self._inspect_frame['text'] = 'inspect:'
        self._canvas_inspector.delete(tkinter.ALL)

    def is_card_on_table(self, card_name: str) -> bool:
        if card_name in self._cards_on_table:
            return True
        else:
            return False

    def update_title(
            self, name: str):
        self._table_frame['text'] = f'current game: {name}'

    def clean_table(self):
        self.clean_inspect_area()
        self._canvas_table.delete(tkinter.ALL)
        self._cards_on_table = dict()

    def update_card_image(
            self,
            card_name: str,
            img_path: str,
            is_locked: bool,
            rotated: bool = False):
        card: dict = self._cards_on_table.get(card_name)
        img: ImageFile.ImageFile = Image.open(img_path)
        card_width = self._table_width / self._TABLE_WIDTH_IN_CARDS
        maxsize = (card_width, self._table_height)
        img.thumbnail(maxsize)
        if rotated:
            img = img.rotate(180)
        card[self._IMG_KEY] = ImageTk.PhotoImage(img)
        label = card[self._IMG_LABEL_KEY]
        label.configure(image=card[self._IMG_KEY])
        if is_locked:
            label['background'] = 'blue'
        else:
            label['background'] = 'green'

    def remove_card(self, card_name: str):
        card: dict = self._cards_on_table.pop(card_name)
        label: tkinter.Label = card[self._IMG_LABEL_KEY]
        label.destroy()

    def update_box_cards_list(self, card_names: list[str]):
        self._boxcards_list.set('')
        self._boxcards_list['values'] = card_names

    def update_deck_cards_list(self, card_names: list[str]):
        self._deckcards_list.set('')
        self._deckcards_list['values'] = card_names

    def update_draw_pile(
            self,
            draw_pile: list[str],
            card: BaseCard | None,
            ):
        self._drawpile['values'] = draw_pile
        if draw_pile:
            self._top_card_label.img = card.path
            img: ImageFile.ImageFile = Image.open(card.path)
            maxsize = (self._menu_width / 2, self._height)
            img.thumbnail(maxsize)
            if rotated:
                img = img.rotate(180)
            self._top_card_label['image'] = ImageTk.PhotoImage(img)

    def update_discarded_pile(self, discarded: list[str]):
        self._discardpile['values'] = discarded


if __name__ == '__main__':
    # gui = TkinterGUI()
    # gui.run()
    import launchers
    launchers.run_pycards()
