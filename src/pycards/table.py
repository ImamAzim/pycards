from pycards.game import Game, GameError
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
        :returns: TODO

        """
        self._gui.clean_table()
        name = self._game.name
        self._gui.update_title(name)
        box_cards_names = self._game.box_card_names
        self._gui.update_box_cards_list(box_cards_names)
        draw_pile = self._game.draw_pile_cards
        self._gui.update_draw_pile(draw_pile)
        
        pass

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
            deck_card_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_card_names)
            card = self._game.get_card(card_name)
            self._gui.place_card_on_table(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    'discard',
                    card.rotate)

    def destroy_card(self, card_name: str):
        try:
            self._game.destroy_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            deck_card_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_card_names)
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
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
                        self._game.is_card_permanent(card_name),
                        card.rotate,
                        )
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
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
                        self._game.is_card_permanent(card_name),
                        card.rotate,
                        )
            self._gui.inspect_card(
                    card_name,
                    card.path,
                    self._game.is_card_permanent(card_name),
                    card.rotate)

    def forget_card(self, card_name: str):
        try:
            self._game.forget_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
        else:
            deck_card_names = self._game.deck_card_names
            self._gui.update_deck_cards_list(deck_card_names)
            box_cards_names = self._game.box_card_names
            self._gui.update_box_cards_list(box_cards_names)
            if self._gui.is_card_on_table(card_name):
                self._gui.remove_card(card_name)
            self._gui.clean_inspect_area()

    def lock_card(self, card_name: str):
        try:
            self._game.lock_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
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
        try:
            self._game.unlock_card(card_name)
        except GameError as e:
            self._gui.showerror(e)
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
        if card_name:
            try:
                card = self._game.get_card(card_name)
            except GameError as e:
                self._gui.showerror(e)
            else:
                self._gui.inspect_card(
                        card_name,
                        card.path,
                        self._game.is_card_permanent(card_name),
                        card.rotate)

    def shuffle_deck(self):
        cards = self._game.shuffle_deck()
        for card in cards:
            if self._gui.is_card_on_table(card.name):
                self._gui.remove_card(card.name)
            self._gui.place_card_on_table(
                    card.name,
                    card.path,
                    False,
                    'deck',
                    card.rotate)
        permanent_cards = self._game.permanent_cards
        for card in permanent_cards:
            if card.name not in self._game.box_card_names:
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
