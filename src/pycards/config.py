import os


import xdg


APP = 'pycards'


DATA_FOLDER = os.path.join(xdg.xdg_data_home(), APP)
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
