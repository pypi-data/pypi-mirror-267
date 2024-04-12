.. nodestack documentation master file, created by
   sphinx-quickstart on Sat Mar 30 18:38:12 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to nodestack's documentation!
=====================================

.. note::

   This project is under active development.

Content:
--------

.. toctree::
   :maxdepth: 2
   
   api

Installation:
-------------
.. code-block:: console

   (venv) $ git clone https://gitea.lutix.org/ftg/nodestack.git

or

.. code-block:: console

   (venv) $ pip install nodestack

Source code is hosted on my own instance of `gitea <https://gitea.lutix.org/ftg/nodestack>`_.

Basic Usage:
------------

.. code-block:: python

   import nodestack

   class Person(nodestack.Node):
       pass

   bob = Person('Bob')
   eve = Person('Eve')
   alice = Person('Alice')
   alice_again = Person('Alice') # will raise an error


   # Alice is parent of bob and eve
   alice.add_child(bob)
   alice.add_child(eve)

   alice.pretty_print()

   Alice
     -- Bob
     -- Eve





