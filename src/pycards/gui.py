import tkinter
from tkinter import simpledialog, filedialog, messagebox
from tkinter import ttk
from typing import Literal
from pathlib import Path
from io import BytesIO


from PIL import Image, ImageTk, ImageFile


from pycards.interfaces import GUI, BaseTable, BaseCard
from pycards.interfaces import IN_PLAY_PILE_NAME, PERMANENT_PILE_NAME


class GUIError(Exception):
    pass


class EditorWindow(simpledialog.Dialog):

    """open a prompt window to edit card image"""

    def __init__(
            self,
            parent: GUI,
            card_name: str,
            img_path: Path | str,
            rotated: bool,
            max_width: int,
            max_height: int,
            ):
        """

        :img_path: TODO
        :rotated: TODO

        """
        self._max_canvas_width = max_width
        self._max_canvas_height = max_height
        self._img_path = Path(img_path)
        self._rotated = rotated
        self._card_name = card_name
        self._save_img = False
        self._used_stickers = dict()

        self._gui = parent

        super().__init__(parent)

    def body(self, master):

        frame = ttk.Labelframe(master, text=self._card_name)
        frame.pack()

        img: ImageFile.ImageFile = Image.open(self._img_path)
        width, height = img.width, img.height
        if self._rotated:
            img = img.rotate(180)
        self._img = ImageTk.PhotoImage(img)
        canvas = tkinter.Canvas(
                frame,
                bg='green',
                height=height,
                width=width,
                )
        canvas.create_image(
                (0, 0),
                anchor=tkinter.NW,
                image=self._img,
                )
        canvas.pack()
        canvas.bind("<Button-1>", self._save_position)
        self.bind("<B1-Motion>", self._add_line)
        self._canvas = canvas
        button_frame = ttk.Frame(master)
        button_frame.pack()
        table: BaseTable = self._gui.table
        self._stickers = table.get_stickers()
        sticker_names = list(self._stickers)
        self._stickers_list = ttk.Combobox(
                master,
                state='readonly',
                values=sticker_names,
                )
        if sticker_names:
            self._stickers_list.set(sticker_names[0])
        self._stickers_list.pack()
        ttk.Button(
                button_frame,
                text='add sticker...',
                command=self._add_sticker,
                ).pack()

    def _add_sticker(self):
        """add sticker

        """
        sticker_name = self._stickers_list.get()
        sticker_names = list(self._stickers_list['values'])
        sticker_names.remove(sticker_name)
        self._stickers_list['values'] = sticker_names
        if sticker_names:
            self._stickers_list.set(sticker_names[0])
        else:
            self._stickers_list.set('')

        img_path = self._stickers[sticker_name]
        img: ImageFile.ImageFile = Image.open(img_path)
        self._used_stickers[sticker_name] = ImageTk.PhotoImage(img)
        window_id = self._canvas.create_image(
                (0, 0),
                anchor=tkinter.NW,
                image=self._used_stickers[sticker_name],
                )
        self._canvas.tag_bind(
                window_id,
                "<ButtonPress-1>",
                lambda e: self._on_sticker_click(e))
        self._canvas.tag_bind(
                window_id,
                "<B1-Motion>",
                lambda e: self._on_sticker_drop(e, window_id))

    def _on_sticker_click(self, event: tkinter.Event):
        self._cursor_x0 = event.x
        self._cursor_y0 = event.y

    def _on_sticker_drop(self, event: tkinter.Event, window_id: int):
        cursor_x = event.x
        cursor_y = event.y
        dx = cursor_x - self._cursor_x0
        dy = cursor_y - self._cursor_y0
        self._canvas.move(window_id, dx, dy)

    def apply(self):
        canvas = self._canvas
        path = self._img_path
        width = self._img.width()
        height = self._img.height()
        eps = canvas.postscript(
                colormode='color',
                width=width,
                height=height,
                pagewidth=width,
                pageheight=height,
                )
        img = Image.open(BytesIO(bytes(eps, 'ascii')))
        img.save(path)
        table: BaseTable = self._gui.table
        for sticker_name in self._used_stickers:
            table.delete_stickers(sticker_name)

    def _save_position(self, event):
        self._lastx, self._lasty = event.x, event.y

    def _add_line(self, event):
        canvas = self._canvas
        x1 = self._lastx
        x2 = event.x
        y1 = self._lasty
        y2 = event.y
        canvas.create_line((x1, y1, x2, y2))
        self._save_position(event)


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
    # TABLE_WIDTH_WEIGHT = 4  # relative wieght to menu column
    # TABLE_REL_HEIGHT = 3  # unit of screen height
    # _PERMANENT_ZONE_HEIGHT = 1 / 4  # of the screen height
    # _TABLE_WIDTH_IN_CARDS = 6
    _NCARDS_PER_TABLE = 6
    _TABLE_WIDTH = 4 / 5
    _TABLE_HEIGHT = 3 / 4
    _INSPECTOR_HEIGHT = 1 / 2
    _TOPCARD_HEIGHT = (1 - _INSPECTOR_HEIGHT) / 2
    _TOPCARD_WIDTH = (1 - _TABLE_WIDTH) / 2
    _IMG_KEY = 'img'
    _IMG_LABEL_KEY = 'img_label'
    _PILE_KEY = 'pile'
    _WINDOW_ID_KEY = 'window_id'
    _EXTENDED_HEIGHT = 3  # for scroll region

    @property
    def table(self) -> BaseTable:
        return self._table

    @table.setter
    def table(self, table: BaseTable):
        self._table = table

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('pycards')
        self._table = None
        self._game_name: str = None
        self._inspected_card = tkinter.StringVar(self)
        self._inspected_card.set(None)
        self._cards_on_table: dict[str, dict] = dict()
        self._gamezone_frame: tkinter.Frame
        self._permanent_frame: tkinter.Frame
        self._cardlist_frame: tkinter.Frame
        self._inspect_frame: tkinter.Frame

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        geometry = f'{width}x{height}'
        self.geometry(geometry)
        self._width = width * 0.93  # available width
        self._height = height * 0.8  # available height

        self._gamezone_height = self._height * self._TABLE_HEIGHT
        self._gamezone_width = self._width * self._TABLE_WIDTH
        self._inspector_height = self._height * self._INSPECTOR_HEIGHT
        self._inspector_width = self._width * (1-self._TABLE_WIDTH)

        self._left_pannel = ttk.Frame(self)
        self._right_pannel = ttk.Frame(self)
        self._left_pannel.pack(side=tkinter.LEFT)
        self._right_pannel.pack(side=tkinter.RIGHT)

        self._create_menu()
        self._create_cardlist_frame()
        self._create_inspect_frame()
        self._create_gamezone_frame()
        self._create_permanent_frame()

        self._place_all_frames()

        self.update()
        # self._table_width = self._canvas_table.winfo_width()
        # self._inspector_width = self._canvas_inspector.winfo_width()
        # self.geometry(geometry)

    def _place_all_frames(self):
        """position all frames in root window

        """
        self._cardlist_frame.pack(fill=tkinter.X)
        self._inspect_frame.pack()
        self._permanent_frame.pack()
        self._gamezone_frame.pack()

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
                label='import stickers',
                command=self._prompt_import_stickers,
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
        game_menu = tkinter.Menu(menubar)
        game_menu.add_command(
                label='discard all',
                command=lambda: self._table.discard_all(),
                )
        game_menu.add_command(
                label='shuffle',
                command=lambda: self._table.shuffle_back(),
                )
        menubar.add_cascade(
                label='Game',
                menu=game_menu,
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
            self._table.import_cards(Path(path))

    def _prompt_import_stickers(self):
        """ask for a folder to import stickers

        """
        path = filedialog.askdirectory(title='select a folder with stickers')
        if path:
            self._table.import_stickers(Path(path))

    def _prompt_load_game(self):
        """present games that can be loaded

        """
        games = self._table.get_saved_games()
        if games:
            prompt = LoadPrompt(self, games)
            game = prompt.game_name
            if game:
                self._table.load_game(game)
        else:
            msg = 'there is no saved game on disk'
            self.showinfo(msg)

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
        self._cardlist_frame = ttk.Frame(self._left_pannel)

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
                fill=tkinter.X,
                expand=True,
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
                row=0,
                sticky=tkinter.EW,
                )
        ttk.Button(
                drawpile_frame,
                text='draw...',
                command=lambda: self._table.draw_card(),
                ).grid(column=0, row=2, sticky='NSEW')
        ttk.Button(
                drawpile_frame,
                text='inspect...',
                command=lambda: self._table.inspect_obfuscated_card(
                    self._drawpile.get()),
                ).grid(column=0, row=1, sticky=tkinter.NSEW)
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
        self._discardpile.pack(fill=tkinter.X)

    def _call_discover(self):
        card_name = self._inspected_card.get()
        self._table.discover_card(card_name)

    def _create_inspect_frame(self):
        """canvas and options

        """
        self._inspect_frame = ttk.LabelFrame(
                self._left_pannel,
                text='inspector')
        self._inspected_card_label = ttk.Label(
                self._inspect_frame,
                )
        self._inspected_card_label.pack()
        buttons_frame = ttk.Frame(self._inspect_frame)
        buttons_frame.pack()
        self._discover_forget_button = ttk.Button(
                buttons_frame,
                text='discover',
                command=lambda: self._table.discover_or_forget(
                    self._inspected_card.get()),
                )
        self._discover_forget_button.grid(row=0, column=0)
        ttk.Button(
                buttons_frame,
                text='destroy',
                command=lambda: self._table.destroy_card(
                    self._inspected_card.get()),
                ).grid(row=0, column=1)
        ttk.Button(
                buttons_frame,
                text='flip',
                command=lambda: self._table.flip(
                    self._inspected_card.get()),
                ).grid(row=0, column=2)
        ttk.Button(
                buttons_frame,
                text='rotate',
                command=lambda: self._table.rotate_card(
                    self._inspected_card.get()),
                ).grid(row=0, column=3)
        self._lock_unlock_button = ttk.Button(
                buttons_frame,
                text='lock',
                command=lambda: self._table.lock_unlock(
                    self._inspected_card.get()),
                )
        self._lock_unlock_button.grid(row=1, column=0)
        ttk.Button(
                buttons_frame,
                text='play',
                command=lambda: self._table.play_card(
                    self._inspected_card.get()),
                ).grid(row=1, column=1)
        ttk.Button(
                buttons_frame,
                text='discard',
                command=lambda: self._table.discard(
                    self._inspected_card.get()),
                ).grid(row=1, column=2)
        self._mark_unmark_button = ttk.Button(
                buttons_frame,
                text='mark',
                command=lambda: self._table.mark_or_unmark(
                    self._inspected_card.get()),
                )
        self._mark_unmark_button.grid(row=1, column=3)
        ttk.Button(
                buttons_frame,
                text='top',
                command=lambda: self._table.put_card_in_draw_pile(
                    self._inspected_card.get(), True),
                ).grid(row=2, column=0)
        ttk.Button(
                buttons_frame,
                text='bottom',
                command=lambda: self._table.put_card_in_draw_pile(
                    self._inspected_card.get(), False),
                ).grid(row=2, column=1)
        ttk.Button(
                buttons_frame,
                text='edit',
                command=lambda: self._table.prompt_editor(
                    self._inspected_card.get()),
                ).grid(row=2, column=2)

    def prompt_editor(
            self,
            card_name: str,
            img_path: str,
            rotated: bool,):
        max_width = self.winfo_screenwidth() // 2
        max_height = self.winfo_screenheight() // 2
        EditorWindow(
                self,
                card_name,
                img_path,
                rotated,
                max_width,
                max_height,)
        self._table.inspect_card(card_name)
        if self.is_card_on_table(card_name):
            self.update_card_image(card_name, img_path, rotated)

    def _create_gamezone_frame(self):
        """ prepare zone where cards will be in play

        """
        self._gamezone_frame = ttk.LabelFrame(
                self._right_pannel,
                text='game zone')
        canvas = tkinter.Canvas(
                self._gamezone_frame,
                bg='green',
                height=self._gamezone_height,
                width=self._gamezone_width,
                scrollregion=(
                    0,
                    0,
                    self._gamezone_width,
                    self._EXTENDED_HEIGHT * self._gamezone_height),
                )
        vbar = ttk.Scrollbar(self._gamezone_frame, orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tkinter.LEFT)
        self._canvas_gamezone = canvas

    def _create_permanent_frame(self):
        """prepare canvas where permanent cards are put

        """
        self._permanent_frame = ttk.LabelFrame(
                self._right_pannel,
                text='permanent cards')
        width = self._gamezone_width
        height = self._height - self._gamezone_height
        canvas = tkinter.Canvas(
                self._permanent_frame,
                bg='blue',
                height=height,
                width=width,
                scrollregion=(
                    0,
                    0,
                    width,
                    self._EXTENDED_HEIGHT * height),
                )
        vbar = ttk.Scrollbar(self._permanent_frame, orient=tkinter.VERTICAL)
        vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tkinter.LEFT)
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

    def run(self):
        self.mainloop()

    def place_card_on_table(
            self,
            card_name: str,
            img_path: str,
            pile: Literal[
                IN_PLAY_PILE_NAME, PERMANENT_PILE_NAME] = IN_PLAY_PILE_NAME,
            rotated: bool = False):

        current_pile = self.is_card_on_table(card_name)
        if current_pile:
            if current_pile == pile:
                return
            else:
                self.remove_card(card_name)

        self._cards_on_table[card_name] = dict()
        placed_card = self._cards_on_table[card_name]

        card_width = self._gamezone_width / self._NCARDS_PER_TABLE

        if pile == IN_PLAY_PILE_NAME:
            canvas = self._canvas_gamezone
            card_height = self._gamezone_height
        elif pile == PERMANENT_PILE_NAME:
            canvas = self._canvas_permanent
            card_height = self._height - self._gamezone_height
        else:
            raise GUIError('pile arg not known')

        maxsize = (card_width, card_height)
        img: ImageFile.ImageFile = Image.open(img_path)
        img.thumbnail(maxsize)
        if rotated:
            img = img.rotate(180)
        placed_card[self._IMG_KEY] = ImageTk.PhotoImage(img)
        card_width = img.width
        card_height = img.height

        x, y = self._find_free_space(card_width, card_height, canvas)

        placed_card[self._PILE_KEY] = pile

        label = tkinter.Label(
                canvas,
                image=placed_card[self._IMG_KEY],
                cursor='hand1',
                )
        placed_card[self._IMG_LABEL_KEY] = label
        window_id = canvas.create_window(
                (x, y),
                anchor=tkinter.NW,
                window=label,
                )
        placed_card[self._WINDOW_ID_KEY] = window_id
        label.bind(
                "<ButtonPress-1>",
                lambda e: self._on_card_click(e, card_name))
        label.bind(
                "<B1-Motion>",
                lambda e: self._on_card_drop(e, card_name))

    def _is_overlapping(
            self,
            canvas: tkinter.Canvas,
            x: int,
            y: int,
            width: int,
            height: int,
            tolerance: int = 5) -> bool:
        """check if there is already a card in this area of the table
        assuming x and y are at NW

        """
        x1 = x + tolerance
        x2 = x1 + width - tolerance
        y1 = y + tolerance
        y2 = y + height - tolerance
        overlapping = canvas.find_overlapping(x1, y1, x2, y2)
        return bool(overlapping)

    def _find_free_space(
            self,
            card_width,
            card_height,
            canvas: tkinter.Canvas,
            ) -> tuple[int, int]:
        """find a position where the table is free of other cards

        """
        if canvas == self._canvas_gamezone:
            height = self._gamezone_height * self._EXTENDED_HEIGHT
        else:
            height = (
                    self._height - self._gamezone_height
                    ) * self._EXTENDED_HEIGHT
        max_rows = int(height // card_height + 1)
        max_columns = int(
                (self._gamezone_width + card_width / 4) // card_width)
        for row in range(max_rows):
            y = int(row * card_height)
            for column in range(max_columns):
                x = int(column * card_width)
                overlapping = self._is_overlapping(
                        canvas,
                        x,
                        y,
                        card_width,
                        card_height,
                        )
                if not overlapping:
                    break
            if not overlapping:
                break
        return x, y

    def _on_card_click(self, event: tkinter.Event, card_name: str):
        self._table.inspect_card(card_name)
        self._cursor_x0 = event.x
        self._cursor_y0 = event.y
        card_label: tkinter.Label = event.widget
        card_label.lift()

    def _on_card_drop(self, event: tkinter.Event, card_name: str):
        placed_card = self._cards_on_table[card_name]
        pile = placed_card[self._PILE_KEY]
        window_id = placed_card[self._WINDOW_ID_KEY]
        if pile == IN_PLAY_PILE_NAME:
            canvas = self._canvas_gamezone
        elif pile == PERMANENT_PILE_NAME:
            canvas = self._canvas_permanent
        cursor_x = event.x
        cursor_y = event.y
        dx = cursor_x - self._cursor_x0
        dy = cursor_y - self._cursor_y0
        canvas.move(window_id, dx, dy)

    def inspect_card(self,
                     card_name: str,
                     img_path: str,
                     in_box: bool,
                     not_marked: bool,
                     not_permanent: bool,
                     rotated: bool = False,):

        self._inspected_card.set(card_name)
        self._inspect_frame['text'] = f'inspect: {card_name}'

        label = self._inspected_card_label
        img: ImageFile.ImageFile = Image.open(img_path)
        maxsize = (self._inspector_width, self._inspector_height)
        img.thumbnail(maxsize)
        if rotated:
            img = img.rotate(180)
        label.img = ImageTk.PhotoImage(img)
        label['image'] = label.img

        text = 'discover' if in_box else 'forget'
        self._discover_forget_button['text'] = text
        text = 'mark' if not_marked else 'unmark'
        self._mark_unmark_button['text'] = text
        text = 'lock' if not_permanent else 'unlock'
        self._lock_unlock_button['text'] = text

    def clean_inspect_area(self):
        self._inspected_card.set(None)
        self._inspect_frame['text'] = 'inspect:'
        self._inspected_card_label['image'] = None
        self._inspected_card_label.img = None
        self._inspect_frame.update()

    def is_card_on_table(self, card_name: str) -> bool:
        if card_name in self._cards_on_table:
            pile = self._cards_on_table[card_name][self._PILE_KEY]
            return pile
        else:
            return False

    def update_title(
            self, name: str):
        self._gamezone_frame['text'] = f'current game: {name}'

    def clean_table(self):
        self.clean_inspect_area()
        self._canvas_gamezone.delete(tkinter.ALL)
        self._canvas_permanent.delete(tkinter.ALL)
        self._cards_on_table = dict()

    def update_card_image(
            self,
            card_name: str,
            img_path: str,
            rotated: bool = False):
        card: dict = self._cards_on_table.get(card_name)
        if not card:
            raise GUIError('card is not on table')
        img: ImageFile.ImageFile = Image.open(img_path)

        pile = self.is_card_on_table(card_name)
        if pile == IN_PLAY_PILE_NAME:
            card_height = self._gamezone_height
        elif pile == PERMANENT_PILE_NAME:
            card_height = self._height - self._gamezone_height
        card_width = self._gamezone_width / self._NCARDS_PER_TABLE

        maxsize = (card_width, card_height)
        img.thumbnail(maxsize)
        if rotated:
            img = img.rotate(180)
        card[self._IMG_KEY] = ImageTk.PhotoImage(img)
        label = card[self._IMG_LABEL_KEY]
        label.configure(image=card[self._IMG_KEY])

    def remove_card(self, card_name: str):
        card: dict = self._cards_on_table.pop(card_name)
        label: tkinter.Label = card[self._IMG_LABEL_KEY]
        label.destroy()
        window_id = card[self._WINDOW_ID_KEY]
        pile = card[self._PILE_KEY]
        if pile == IN_PLAY_PILE_NAME:
            canvas = self._canvas_gamezone
        elif pile == PERMANENT_PILE_NAME:
            canvas = self._canvas_permanent
        window_id = card[self._WINDOW_ID_KEY]
        canvas.delete(window_id)

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
        self._drawpile.set('')
        self._drawpile['values'] = draw_pile[-1::-1]
        if draw_pile:
            img: ImageFile.ImageFile = Image.open(card.path)
            width = self._width * self._TOPCARD_WIDTH
            height = self._height * self._TOPCARD_HEIGHT
            maxsize = (width, height)
            img.thumbnail(maxsize)
            if card.rotate:
                img = img.rotate(180)
            self._top_card_label.img = ImageTk.PhotoImage(img)
            self._top_card_label['image'] = self._top_card_label.img
        else:
            self._top_card_label.img = None
            self._top_card_label['image'] = None
            self._top_card_label.update()

    def update_discarded_pile(self, discarded: list[str]):
        self._discardpile.set('')
        self._discardpile['values'] = discarded


if __name__ == '__main__':
    # gui = TkinterGUI()
    # gui.run()
    import launchers
    launchers.run_pycards()
