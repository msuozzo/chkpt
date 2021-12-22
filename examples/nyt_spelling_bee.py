"""A solver for the New York Times Spelling Bee game."""

import collections
import itertools
import os
import re
from urllib import request

import chkpt


@chkpt.Stage.wrap()
def word_list():
  words = request.urlopen('https://github.com/redbo/scrabble/raw/master/dictionary.txt').read().decode('utf8')
  return words.strip().splitlines()


@chkpt.Stage.wrap()
def todays_letters():
  sanitize = lambda s: list(map(str.upper, re.findall(r'[a-zA-Z]', s)))
  while True:
    center = sanitize(input('Enter center letter> '))
    if len(center) == 1:
      break
  while True:
    others = sanitize(input('Enter surrounding letters> '))
    if len(others) == 6:
      break
  return center + others


@chkpt.Stage.wrap()
def candidates(words, letters):
  by_letters = collections.defaultdict(list)
  for word in words:
    if len(word) > 3:
      by_letters[frozenset(word)].append(word)
  return list(
      sorted(
          itertools.chain.from_iterable(
              ws for lets, ws in by_letters.items()
              if letters[0] in lets and lets.issubset(set(letters)))))


if __name__ == '__main__':
  pipeline = (word_list, todays_letters) >> candidates
  matches = pipeline(chkpt.Config(store=[word_list]))
  print(f'Found {len(matches)} matches')
  print(os.linesep.join(matches))
