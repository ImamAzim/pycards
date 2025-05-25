class Card(object):

    """Card class to handle a single card"""

    @property
    def state(self) -> int:
        """orientation of the card (4 values possible)"""
        return self._state

    @property
    def recto_img(self) -> str:
        """path location of img file of recto side"""
        return self._recto_img

    @property
    def verso_img(self) -> str:
        """path location of img file, verso side"""
        return self._verso_img

    def __init__(self):
        """TODO: to be defined. """
        pass


if __name__ == '__main__':
    pass
