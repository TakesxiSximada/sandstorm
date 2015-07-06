sandstorm

The sandstorm is Web Application Framework on Tornado, but can use Pyramid like.

.. image:: https://circleci.com/gh/TakesxiSximada/sandstorm.svg?style=svg
               :target: https://circleci.com/gh/TakesxiSximada/sandstorm

Install
===========

execute command::

    $ pip install sandstorm


How to use
===========

Setting
-----------

Database Setting::

    $ alembic init alembic

alembic.ini::

  [application]
  # your service package name
  module = mypkg

  # api url root prefix
  route_prefix = api

  # debug mode
  debug = True

  # port number
  port = 8000

  # cookie secret
  cookie_secret = __TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__

  # frontend directory
  frontend = ./frontend

  # database section
  db_section = alembic

  # database alias
  db_alias = default


  [alembic]
  script_location = alembic
  sqlalchemy.url = sqlite:///var/db/baast.db

  # ...and more


Start server
---------------


::

    $ sandstorm.server
