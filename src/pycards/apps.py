from pycards.gui import TkinterGUI
from pycards.interfaces import GUI


class PycarApp(object):

    """pycards app that will use mvc model"""

    def __init__(self):
        """init mvc model """
        self._gui:  GUI|TkinterGUI = TkinterGUI()
        table = Table(self._gui)
        self._gui.set_table(table)
        self._gui.place_card_on_table

    def start(self):
        """start the pycard app

        """
        self._gui.run()
