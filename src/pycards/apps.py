from pycards.gui import TkinterGUI


class PycarApp(object):

    """pycards app that will use mvc model"""

    def __init__(self):
        """init mvc model """
        self._gui = TkinterGUI()
        table = Table(self._gui)
        self._gui.set_table(table)

    def start(self):
        """start the pycard app

        """
        self._gui.run()
