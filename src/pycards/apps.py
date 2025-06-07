from pycards.gui import GUI
from pycards.table import Table


class PycarApp(object):

    """pycards app that will use mvc model"""

    def __init__(self):
        """init mvc model """
        self._gui = GUI()
        table = Table(self._gui)
        self._gui.set_table(table)

    def start(self):
        """start the pycard app

        """
        pass
