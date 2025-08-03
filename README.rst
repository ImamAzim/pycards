under development...

pycards
===================

GUI to play your favorite card game. The rules are not coded, but it allows to manipulate a deck of card, shuffle them, discover, destroy or lock single cards. You can import any set of cards (not included here).
The idea is to reset a legacy card game, instead of buying a new one and you still keep the legacy part. Here is how it could look (with sample cards from arcmage as an example):

.. image:: pycards_screenshot.png
   :width: 600

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

How to play
=============

* start a new game (or load a previous one) with the file menu on top
* at the beginning, there are no cards, you need to import some with the file menu (as if you were buying them). There are no cards included, so you need to create them or download from other sources.
* when the cards are imported, they are in the "box" and you can inspect them but are not yet part of your deck. You need to "discover" them, so that they will be part of your your deck
* cards from your deck will be either in the draw pile, discard pile, game zone or permanent zone.
* with the inspector, your can manipulate your cards (change pile, rotate, flip, edit, etc...)
* when cards are in the game or permanent zone, they can be moved with drag and drop.
* the first card on the draw pile is immediately visible, not the rest. (but you can inspect them if you want).
* with the Game menu, you can put all the cards from the discard pile in the draw pile and shuffle them.

Documentation of all options in the GUI
=======================================

File Menu
-----------

all general options to modify your game:

* **new game**:
* **load game**:
* **delete active game**:
* **import cards**:
* **import stickers**:
* **quit**:


Game Menu
----------

options to manipulate all cards at once:

* **discard all**:
* **shuffle**:

Box cards
----------

Draw pile
----------

Discard Pile
-------------

inspector
----------

game zone
----------

permanent card zone
--------------------


License
=======

The project is licensed under GNU GENERAL PUBLIC LICENSE v3.0
