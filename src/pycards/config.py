import os
from pathlib import Path


import xdg


APP = 'pycards'


DATA_FOLDER = xdg.xdg_data_home() / APP
if not DATA_FOLDER.exists():
    DATA_FOLDER.mkdir()
