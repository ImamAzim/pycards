from pycards.game import Game, GameError, Card
from pycards.interfaces import GUI, BaseTable


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
        self._gui.update_discarded_pile(discarded)
        in_play_cards = self._game.in_play_cards
        for card in in_play_cards:
            card: Card
            self._gui.place_card_on_table(
                    card_name=card.name,
                    img_path=card.path,
                    pile='game_zone',
                    rotated=card.rotate,
                    )
        permanent_cards = self._game.permanent_cards
        for card in permanent_cards:
            card: Card
            self._gui.place_card_on_table(
                    card_name=card.name,
                    img_path=card.path,
                    pile='permanent',
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

    def import_cards(self, folder_path: str):
        try:
            self._game.import_cards_folder(folder_path)
        except GameError as e:
            self._gui.showerror(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)

    def discover_card(self, card_name: str):
        try:
            self._game.discover_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            discarded = self._game.discarded_cards
            self._gui.update_discarded_pile(discarded)

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
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    card.rotate)

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
            self._gui.inspect_card(
                    card_name,
                    card.path,
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
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)
            self._gui.clean_inspect_area()

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
            self._gui.update_discarded_pile(discard_pile)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    'permanent',
                    )

    def unlock_card(self, card_name: str):
        try:
            self._game.unlock_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            discard_pile = self._game.discarded_cards
            self._gui.update_discarded_pile(discard_pile)
            self._gui.remove_card(card_name)

    def inspect_card(self, card_name: str):
        if card_name:
            try:
                card = self._game.get_card(card_name)
            except GameError as e:
                self._gui.showerror(e)
            else:
                self._gui.inspect_card(
                        card_name,
                        card.path,
                        card.rotate)

    def inspect_card(self, card_name: str):
        if card_name:
            try:
                card = self._game.get_card(card_name)
            except GameError as e:
                self._gui.showerror(e)
            else:
                self._gui.inspect_card(
                        card_name,
                        card.path,
                        card.rotate)

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
            self._gui.update_discarded_pile(discard_pile)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    'game_zone',
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
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)

    def mark_card(self, card_name: str):
        try:
            self._game.set_always_visible(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)

    def unmark_card(self, card_name: str):
        try:
            self._game.remove_always_visible(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            draw_pile = self._game.draw_pile_cards
            top_card = self._game.get_draw_pile_top_card()
            self._gui.update_draw_pile(draw_pile, top_card)

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
            self._gui.update_discarded_pile(discard_pile)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)

    def discard_all(self):
        for card_name in self._game.in_play_cards:
            self._game.discard(card_name)
            self._gui.remove_card(card_name)
        discard_pile = self._game.discarded_cards
        self._gui.update_discarded_pile(discard_pile)

    def draw_card(self):
        try:
            self._game.play_first_card()
        except GameError as e:
            self._gui.showerror(e)

    def shuffle_back(self):
        self._gui.clean_inspect_area()


if __name__ == '__main__':
    pass
