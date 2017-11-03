# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import pickle, os, sys, subprocess, datetime, requests

from lib.player import Player
from lib.comp import AIOpponent

def save(game):
  if not os.path.exists('./saves'):
    os.mkdir('./saves')

  filename = ask_filename(game)

  while os.path.exists('./saves/' + filename + '.pickle'):
    game.current_player.output.write('\n' + filename +  ' already exists.\n')
    game.current_player.output.flush()
    filename = ask_filename(game)

  players_list = []

  for p in game.players_list:
    players_list.append([p.name, p.score, p.letters, type(p).__name__ == 'AIOpponent'])

  data = {}
  data['board'] = game.board
  data['bag'] = game.bag
  data['turns'] = game.turns - 1
  data['passes'] = game.passes
  data['points'] = game.points
  data['words'] = game.words
  data['word'] = game.word
  data['time_limit'] = game.time_limit
  data['challenge_mode'] = game.challenge_mode
  data['players'] = game.players
  data['players_info'] = players_list
  data['comp_game'] = game.comp_game
  data['words_list'] = game.words_list
  data['save_meaning'] = game.save_meaning

  file = open('./saves/' + filename + '.pickle', 'wb')
  pickle.dump(data, file)

def load(game):
  if not os.path.exists('./saves'):
    print('\nThere are no save files. Starting a new game...')
    start_anew(game)

  file_list = subprocess.check_output('ls saves | grep pickle', shell=True)

  print('\nFiles in the saves folder:\n')
  print(file_list[:-1].decode('utf-8'))

  filename = input('\nWhat is the name of your file without .pickle? ')

  if not os.path.exists('./saves/' + filename + '.pickle'):
    print('\nNo such file. Starting a new game...')
    start_anew(game)

  file = open('./saves/' + filename + '.pickle', 'rb')
  data = pickle.load(file)

  game.board = data['board']
  game.bag = data['bag']
  game.turns = data['turns']
  game.passes = data['passes']
  game.points = data['points']
  game.words = data['words']
  game.word = data['word']
  game.time_limit = data['time_limit']
  game.challenge_mode = data['challenge_mode']
  game.players = data['players']
  game.comp_game = data['comp_game']
  game.words_list = data['words_list']
  game.save_meaning = data['save_meaning']

  for p in data['players_info']:
    if p[3]:
      player = AIOpponent()
    elif game.comp_game:
      player = Player()
      game.human = player
    else:
      player = Player()

    player.name = p[0]
    player.score = p[1]
    player.letters = p[2]
    game.players_list.append(player)

def ask_filename(game):
  game.current_player.output.write('\nGive a name to the save file: \n')
  game.current_player.output.flush()
  filename = game.current_player.input.readline()[:-1]
  return filename

def start_anew(game):
  os.system('sleep 1')
  game.load_game = False
  game.enter_game_loop()

def get_meaning(words):
  file = open('words.txt', 'a+')
  file.write('\n=== {} ==='.format(datetime.datetime.now()))

  for word in words:
    file.write('\n#' + word.upper() + '#\n')
    try:
      r = requests.get(url='http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=' + word).json()

      for result in r['results']:
        file.write('\n\t{} = {}\n'.format(result['headword'], result['senses'][0]['definition'][0]))

        examples = result["senses"][0].get("examples", None)

        if examples:
          file.write('\t\tEXP: {}\n'.format(examples[0]['text']))
    except requests.exceptions.ConnectionError:
      file.write('\n!!! NO CONNECTION !!!\n')
    except KeyError:
      file.write('\n!!! UNABLE TO GET DEFINITION !!!\n')