class Table(object):

    """Table class to create and load games"""
    _active_game = None


    def new_game(self, path: str):
        """create an instance of a game, activate it on the table and save it

        :path: to save the game
        """
        pass

    def load_game(self, path: str):
        """make a game that was previousely saved active
        on the table

        :path: location of game to load
        """
        pass


if __name__ == '__main__':
    pass
