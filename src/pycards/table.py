from pathlib import Path


from pycards.game import Game, GameError, Card
from pycards.interfaces import GUI, BaseTable
from pycards.interfaces import IN_PLAY_PILE_NAME, PERMANENT_PILE_NAME


class Table(BaseTable):

    def __init__(self, gui: GUI):
        self._gui = gui
        self._game = Game()

    def get_saved_games(self) -> [str]:
        """get a list of saved games on disk
        :returns: list of saved games on disk

        """
        games = Game.get_saved_game()
        return games

    def get_current_game(self) -> [str]:
        return self._game.name

    def _update_gui_to_game(self):
        """

        """
        self._gui.clean_table()
        name = self._game.name
        self._gui.update_title(name)
        box_cards_names = self._game.box_card_names
        self._gui.update_box_cards_list(box_cards_names)
        draw_pile = self._game.draw_pile_cards
        top_card = self._game.get_draw_pile_top_card()
        self._gui.update_draw_pile(draw_pile, top_card)
        discarded = self._game.discarded_cards
        discarded = list(discarded)
        self._gui.update_discarded_pile(discarded)
        in_play_cards = self._game.in_play_cards
        for card_name, card in in_play_cards.items():
            card: Card
            self._gui.place_card_on_table(
                    card_name=card.name,
                    img_path=card.path,
                    pile=IN_PLAY_PILE_NAME,
                    rotated=card.rotate,
                    )
        permanent_cards = self._game.permanent_cards
        for card_name, card in permanent_cards.items():
            card: Card
            self._gui.place_card_on_table(
                    card_name=card.name,
                    img_path=card.path,
                    pile=PERMANENT_PILE_NAME,
                    rotated=card.rotate,
                    )

    def delete_game(self):
        try:
            self._game.delete_game()
        except GameError as e:
            self._gui.showerror(e)
        else:
            self._update_gui_to_game()

    def new_game(self, name: str):
        try:
            self._game.new(name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            self._update_gui_to_game()

    def load_game(self, name: str):
        try:
            self._game.load(name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            self._update_gui_to_game()

    def import_cards(self, folder_path: Path):
        try:
            self._game.import_cards_folder(folder_path)
        except GameError as e:
            self._gui.showerror(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)

    def import_stickers(self, folder_path: Path):
        try:
            self._game.import_sticker_folders(folder_path)
        except GameError as e:
            self._gui.showerror(e)

    def discover_or_forget(self, card_name):
        if card_name in self._game.box_card_names:
            self.discover_card(card_name)
        else:
            self.forget_card(card_name)

    def discover_card(self, card_name: str):
        try:
            self._game.discover_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            discarded = self._game.discarded_cards
            discarded = list(discarded)
            self._gui.update_discarded_pile(discarded)
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            card = self._game.get_card(card_name)
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate,
                    )

    def prompt_editor(self, card_name: str):
        if card_name:
            card = self._game.get_card(card_name)
            self._gui.prompt_editor(
                    card_name,
                    card.path,
                    card.rotate,
                    )

    def get_stickers(self):
        return self._game.stickers

    def delete_stickers(self, sticker_name: str):
        try:
            self._game.delete_sticker(sticker_name)
        except GameError as e:
            self._gui.showerror(e)

    def destroy_card(self, card_name: str):
        try:
            self._game.destroy_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)
            self._gui.clean_inspect_area()

    def rotate_card(self, card_name):
        try:
            self._game.rotate_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            card = self._game.get_card(card_name)
            if self._gui.is_card_on_table(card_name):
                self._gui.update_card_image(
                        card_name,
                        card.path,
                        card.rotate,
                        )
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate,
                    )

    def flip(self, card_name):
        try:
            self._game.flip_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            card = self._game.get_card(card_name)
            if self._gui.is_card_on_table(card_name):
                self._gui.update_card_image(
                        card_name,
                        card.path,
                        card.rotate,
                        )
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate)

    def forget_card(self, card_name: str):
        try:
            self._game.forget_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)
            self._gui.clean_inspect_area()

    def lock_unlock(self, card_name):
        if card_name in self._game.permanent_cards:
            self.unlock_card(card_name)
        else:
            self.lock_card(card_name)

    def lock_card(self, card_name: str):
        try:
            self._game.lock_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    PERMANENT_PILE_NAME,
                    rotated=card.rotate,
                    )
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate,
                    )

    def unlock_card(self, card_name: str):
        try:
            self._game.unlock_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            self._gui.remove_card(card_name)
            card = self._game.get_card(card_name)
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate,
                    )

    def inspect_card(self, card_name: str):
        if card_name:
            try:
                card = self._game.get_card(card_name)
            except GameError as e:
                self._gui.showerror(e)
            else:
                in_box = card_name in self._game.box_card_names
                not_marked = not self._game.is_card_marked(card_name)
                not_permanent = card_name not in self._game.permanent_cards
                self._gui.inspect_card(
                        card_name,
                        card.path,
                        in_box,
                        not_marked,
                        not_permanent,
                        card.rotate)

    def inspect_obfuscated_card(self, obfuscated_name: str):
        if obfuscated_name:
            try:
                card_name = self._game.get_real_card_name(obfuscated_name)
            except GameError as e:
                self._gui.showerror(e)
            else:
                self.inspect_card(card_name)

    def play_card(self, card_name: str):
        try:
            self._game.play_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    IN_PLAY_PILE_NAME,
                    rotated=card.rotate,
                    )

    def discard(self, card_name: str):
        try:
            self._game.discard(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)

    def mark_or_unmark(self, card_name):
        try:
            is_card_marked = self._game.is_card_marked(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            if not is_card_marked:
                self.mark_card(card_name)
            else:
                self.unmark_card(card_name)

    def mark_card(self, card_name: str):
        try:
            self._game.set_always_visible(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            card = self._game.get_card(card_name)
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate,
                    )

    def unmark_card(self, card_name: str):
        try:
            self._game.remove_always_visible(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            in_box = card_name in self._game.box_card_names
            not_marked = not self._game.is_card_marked(card_name)
            not_permanent = card_name not in self._game.permanent_cards
            card = self._game.get_card(card_name)
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    in_box,
                    not_marked,
                    not_permanent,
                    card.rotate,
                    )

    def put_card_in_draw_pile(self, card_name: str, top: bool):
        try:
            self._game.put_card_in_draw_pile(card_name, top=top)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)

    def discard_all(self):
        for card_name in self._game.in_play_cards:
            self._game.discard(card_name)
            self._gui.remove_card(card_name)
        discard_pile = self._game.discarded_cards
        discard_pile = list(discard_pile)
        self._gui.update_discarded_pile(discard_pile)

    def draw_card(self):
        try:
            card_name = self._game.play_first_card()
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    IN_PLAY_PILE_NAME,
                    rotated=card.rotate,
                    )

    def shuffle_back(self):
        try:
            self._game.shuffle_back_all_discarded()
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)
            discard_pile = self._game.discarded_cards
            discard_pile = list(discard_pile)
            self._gui.update_discarded_pile(discard_pile)
            self._gui.clean_inspect_area()


if __name__ == '__main__':
    pass
