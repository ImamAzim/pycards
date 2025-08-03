under development...

pycards
===================

GUI to play your favorite card game. The rules are not coded, but it allows to manipulate a deck of card, shuffle them, discover, destroy or lock single cards. You can import any set of cards (not included here).
The idea is to reset a legacy card game, instead of buying a new one and you still keep the legacy part. Here is how it looks:

img

Requirements
===============

* python 3.7
* it was developped on ubuntu linux and the installation procedure is described with this system. However, it should also probably work on windows


Installation
============

preferably in a virtual environement, simply do:

.. code-block:: bash

    pip install git+https://github.com/ImamAzim/pycards.git

and to run the game:

.. code-block:: bash

    pycards

Usage
=====

.. code-block:: bash
    pycards

Features
========

* import a set cards (image files, recto verso), as if you "buy" them
* save/load a game
* discover card from the deck
* forget cards 
* destroy cards
* move cards on a table
* rotate cards
* shuffle
* make permanent card (will no be shuffled)


License
=======

The project is licensed under GNU GENERAL PUBLIC LICENSE v3.0
