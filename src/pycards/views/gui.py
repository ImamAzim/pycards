from abc import ABC, abstractmethod


class GUI(ABC):

    """GUI for a pycards game"""

    def __init__(self):
        """TODO: to be defined. """
        ABC.__init__(self)

    @abstractmethod
    def refresh(self, arg1):
        """TODO: Docstring for refresh.

        :arg1: TODO
        :returns: TODO

        """
        pass


class TkinterGUI(GUI):

    """Docstring for TkinterGUI. """

    def __init__(self):
        """TODO: to be defined. """
        GUI.__init__(self)

