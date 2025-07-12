from pycards.table import Table
from pycards.gui import TkinterGUI
from pycards.interfaces import GUI, BaseTable


class PycarApp(object):

    """pycards app that will use mvc model"""

    def __init__(self):
        """init mvc model """
        self._gui:  GUI | TkinterGUI = TkinterGUI()
        table: BaseTable = Table(self._gui)
        self._gui.table = table
        self._gui.place_card_on_table

    def start(self):
        """start the pycard app

        """
        self._gui.run()
