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

* **new game**: enter your name and new game will be created
* **load game**: select from the list a previous game to load (note: there is no save options, because every changes are always saved. you cannot undo permanent change, as in a legay game)
* **delete active game**: delete the current game from disk
* **import cards**: select a folder that contains all your cards to be imported. it needs to be image files. filename will be used to name cards. There is always a recto and a verso, so you need 2 image file for each card. alphabetic order is used to guess the verso, so you can name it *card_1.png* and *card_1_verso.png* for example.
* **import stickers**: select a folder containing stickers that can be sticked on cards later. it must be image files. you need multiple copy of the same image if you are going to stick it several times
* **quit**: quit the GUI.


Game Menu
----------

options to manipulate all cards at once:

* **discard all**: put all the cards from the game zone in the discard pile
* **shuffle**: put all the cards from the discard pile in the draw pile and shuffle the order.

game zone
----------

in this green zone, the card can be drag and dropped. when you click on one, it is visible in the **inspector**
a slider on the right allows to move the view.

permanent card zone
--------------------

in this blue zone, the card can be drag and dropped. when you click on one, it is visible in the **inspector**.
a slider on the right allows to move the view.

Box cards
----------

Here, there is a list of all the cards from your box. In the list you can only see the name, but not the image. When you click on *inspect*, the selected card will be visible in the **inspector** (see below) and you can manipulate it or transfer it to your deck.

Draw pile
----------

this represent your draw pile. the list contains all the cards, but with an obfuscated name, since they are hidden in the pile. Only the first card is visible (right). There also 2 action buttons:

* **draw**: put the first card of the pile in the game zone.
* **inspect**: make the slected card visible in the **inspector** (see below)

Discard Pile
-------------

a list of discarded cards. when you select one from the list, it is automaticelly visible in the **inspector**

inspector
----------

you can see in detail the inspected cards and use the following actions on it:

* **discover/forget**: move the card from the box to the deck, or vice-versa
* **destroy**: remove the card from the game completely. it cannot be recovered again. (unless you *import* it again).
* **flip**: flip the card between recto and verso
* **rotate**: rotate by 180 degrees the cards
* **lock/unlock**: put the card in the permanent cards zone (or remove it from). When a card is permanent, is cannot be placed into the draw pile nor cannot it be discarded.
* **play**: put the card in the game zone
* **discard**: put the card in the discard pile
* **mark/unmark**: put/remove a marker on the card. When marked, a card can always be identified, even inside the draw pile.
* **top**: put the card on the top of the draw pile.
* **bottom**: put the card in the bottom of the draw pile
* **edit**: open *editor* for the card. (see below)

Editor
---------

* you can draw anything on the card with the mouse
* press ok or cancel to confirm or cancel the changes
* if you have imported stickers, you can select one from the list and add it (*add sticker...*). the sticker appears in the corner and you can drag and drop it on the card. 

License
=======

The project is licensed under GNU GENERAL PUBLIC LICENSE v3.0
