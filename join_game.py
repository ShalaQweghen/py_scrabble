# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

from lib.lan_helpers import join_game

try:
  join_game(sys.argv[1])
except IndexError:
  print('Usage: python3 join_game.py <ip_address>\n       python3 join_game.py auto')