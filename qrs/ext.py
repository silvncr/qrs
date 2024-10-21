from __future__ import annotations

from json import loads
from os import path

# get full wordlist from file
with open(path.join(path.dirname(__file__), 'wordlist.txt')) as f:
	wordlist_full: set[str] = set(f.read().splitlines())
max_length_full: int = max(len(word) for word in wordlist_full)

# set games with respective letter scores
with open(path.join(path.dirname(__file__), 'letter_scores.json')) as f:
	letter_scores: dict[str, dict[str, int]] = loads(f.read())
