'''
Provides word game-related tools that can be configured with custom settings, letter scores, and wordlists.
'''

# imports
from contextlib import suppress
from copy import deepcopy
from json import decoder, dumps, load
from os import path
from string import ascii_lowercase
from sys import path as syspath
from typing import Any, Dict, List, Optional, Tuple, Union

# metadata
__author__ = 'silvncr'
__license__ = 'MIT'
__module_name__ = 'qrs'
__python_version__ = '3.6'
__version__ = '1.2.0'


# get full wordlist from file
wordlist_full = sorted(
	open(
		path.join(
			path.dirname(__file__), 'wordlist.txt'
		)
	).read().strip().split('\n')
)

# command-line arguments; formatted as (arg, sarg, type, default, multiple, help)
kwargs = [
	('debug', 'd', bool, False, ..., 'Whether to display debug information'),
	('exclude', 'e', str, [], True, 'Words to exclude'),
	('game', 'g', str, 'quarrel', None, 'Scoring system to use'),
	('include', 'i', str, [], True, 'Words to include'),
	('lower', 'l', bool, False, ..., 'Whether output should be lowercase'),
	('max', 'm', int, max(len(word) for word in wordlist_full), None, 'Maximum length of words'),
	('min', 'n', int, 2, None, 'Minimum length of words'),
	('noscores', 's', bool, False, ..., 'Whether to ignore scores'),
	('repeats', 'r', bool, False, ..., 'Whether letters are allowed to repeat'),
]

# get letter scores for name
def build_letter_scores(
	name: Optional[str] = None,
) -> Dict[str, int]:
	'''
	Returns the letter scores for the given name. To be passed into the `Ruleset` class.

	Args:
		`name: str` (optional): The name of the letter scoring system. Defaults to *Quarrel*.

	Returns:
		`dict[str, int]`: A dictionary of letter scores, with letters as keys and scores as values, or an empty dictionary if `name` is invalid.
	'''

	# name default
	if not name:
		name = 'quarrel'

	# return letter scores
	return next(
		(
			val for key, val in {
				'quarrel': {
					'a': 1, 'b': 5, 'c': 2, 'd': 3, 'e': 1, 'f': 5, 'g': 4,
					'h': 4, 'i': 1, 'j': 15, 'k': 6, 'l': 2, 'm': 4, 'n': 1,
					'o': 1, 'p': 3, 'q': 15, 'r': 2, 's': 1, 't': 1, 'u': 3,
					'v': 6, 'w': 5, 'x': 10, 'y': 5, 'z': 12
				},
				'scrabble': {
					'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
					'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
					'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
					'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
				},
			}.items() if name == key
		), {}
	)

# get query string
def build_query(
	query: str,
	repeat_letters: bool = True,
) -> str:
	'''
	Returns a sorted query string, with optional repeats.

	Args:
		`query: str`: Query string to sort.
		`repeat_letters: bool` (optional): Whether to allow repeating letters in the query string. Usually the *opposite* of `Ruleset()['repeats']`. Defaults to True.

	Returns:
		`str`: The inputted query string, but sorted.
	'''

	# return query string
	return ''.join(
		sorted(query)
		if repeat_letters
		else sorted(list(set(dict.fromkeys(query))))
	).lower()

# get settings object from settings
def build_settings(
	user_settings: 'Optional[dict[str, Any]]' = None,
	wordlist: 'Optional[list[str]]' = None,
) -> Dict[str, Any]:
	'''
	Returns the settings for the given user settings. To be passsed into the `Ruleset` class.

	Args:
		`user_settings: dict[str, Any]` (optional): Custom settings to override the default settings. Defaults to an empty dictionary.
		`wordlist: list[str]` (optional): Wordlist used to determine defaults for word-related settings.

	Returns:
		`dict[str, Any]`: A dictionary of settings.
	'''

	# user_settings default
	if not user_settings:
		user_settings = {}

	# wordlist default
	if not wordlist:
		wordlist = wordlist_full

	# remove excluded words
	if 'exclude' in user_settings:
		for word in user_settings['exclude']:
			if (word) and (word in wordlist):
				wordlist.remove(word)

	# add included words
	if 'include' in user_settings:
		for word in user_settings['include']:
			if (word) and (word not in wordlist):
				wordlist.append(word)

	# build defaults
	settings = {
		**{str(arg): default for arg, _, _, default, _, _ in kwargs},
		**user_settings,
		'min': max(user_settings['min'], 2) if 'min' in user_settings else 2,
		'max': min(user_settings['max'], max(len(word) for word in wordlist))
		if 'max' in user_settings
		else max(len(word) for word in wordlist),
	}

	# set min-max
	return {
		**settings, **{
			'game': str(
				settings['game']
				if build_letter_scores(settings['game'])
				else 'quarrel'
			)
		}
	}

# word game ruleset class
class Ruleset:
	def __init__(
		self,
		settings: 'Optional[dict[str, Any]]' = None,
		wordlist: 'Optional[list[str]]' = None,
	) -> None:
		'''
		Defines a word game ruleset with the given settings and wordlist.

		Args:
			`settings: dict[str, Any]` (optional): Custom settings to override the default settings. Should be an output from `build_settings()`. Defaults to an empty dictionary.
			`wordlist: list[str]` (optional): A list of words to be used in the ruleset. Defaults to the full Scrabble wordlist.

		Returns:
			A `Ruleset` with the specified settings and wordlist.
		'''

		# settings default
		settings = settings or {}

		# wordlist default
		wordlist = wordlist or wordlist_full

		# remove excluded words
		if 'exclude' in settings:
			for word in settings['exclude']:
				if (word) and (word in wordlist):
					wordlist.remove(word)

		# add included words
		if 'include' in settings:
			for word in settings['include']:
				if (word) and (word not in wordlist):
					wordlist.append(word)

		# get settings
		settings = build_settings(settings, wordlist)

		# adjust wordlist to settings
		wordlist = [
			word for word in wordlist
			if settings['min'] <= len(word) <= settings['max']
		]

		# set attributes
		self.settings = settings
		self.scores = {
			word: sum(build_letter_scores(self['game'])[char] for char in word)
			for word in sorted(
				sorted(wordlist),
				key=lambda word: (
					len(word), sum(
						build_letter_scores(self['game'])[char]
						for char in word
					)
				), reverse=True
			)
		}
		self.wordlist = wordlist

	# getitem method
	def __getitem__(self, key: str) -> Any:
		'''
		Returns the value of the given setting, as defined in the ruleset's settings.

		Args:
			`key: str`: The setting to get the value of.

		Returns:
			`Any`: The value of the given setting.
		'''

		# return setting, or raise error
		if key in self.settings.keys():
			return self.settings[key]
		else:
			raise KeyError(f'{key} not found in settings')

	# get settings
	def get_settings(
		self,
	) -> Dict[str, Any]:
		'''
		Returns the current settings.
		'''

		# return settings object
		return self.settings

	# get settings as string
	def get_settings_str(
		self,
	) -> str:
		'''
		Returns the current settings as a JSON string, formatted with tabs.
		'''

		# return settings string
		return dumps(self.settings, indent=2, sort_keys=True).replace('  ', '\t')

	# solve function
	def solve(
		self,
		query: str,
	) -> Tuple[Dict[int, List[Union[List[str], str]]], bool]:
		'''
		Finds all possible words that can be formed from the given query string using the set wordlist.

		Args:
			`query: str`: A string representing the query to be solved.

		Returns:
			`tuple`: A tuple containing a dictionary of best words by length, and a boolean indicating whether an anagram was found.
		'''

		# build query
		query = build_query(query, not self['repeats'])

		# initialise output object
		scores = {}

		# prepare debug output
		if self['debug']:
			print('')

		# iterate through possible word lengths
		for len_iter in range(
			2, (self['max'] if self['repeats'] else len(query)) + 1
		)[::-1]:
			scores = {
				**scores, **{
					len_iter: [[], 0]
				}
			}

			# iterate through wordlist
			for word in self.scores:
				query_iter, word_iter = deepcopy(query), deepcopy(word)
				word_fits = False

				# handle ignore_scores
				if (
					len(word) == len_iter if self['noscores'] else len(word) <= len_iter
				) and set(word) <= set(query):
					if not self['noscores'] and self.scores[word] < scores[len_iter][1]:
						continue

					# handle allow_repeats
					if self['repeats']:
						word_fits = all(char in query for char in word)

					# iterate through letters
					else:
						for char in word:
							query_iter = query_iter.replace(char, ' ', 1)
							word_iter = word_iter.replace(char, ' ', 1)

							# debug info
							if self['debug']:
								print(f'input: {[query_iter]} | {[word]}: {[word_iter]}')

						# check if word fits
						if query_iter.count(' ') == word_iter.count(' ') != 0:
							word_fits = True

							# debug info
							if self['debug']:
								print(f'{[word]} fits for {[len_iter]}')

				# add word to output
				if word_fits:
					scores[len_iter][0].append(word)

					# update score
					if not self['noscores']:
						scores[len_iter][1] = self.scores[scores[len_iter][0][0]]

			# debug info
			if self['debug']:
				print(f' - output for {[len_iter]}: {scores[len_iter][0]}')

		# determine whether an anagram was found
		try:
			anagram_found = len(scores[len(query)][0][0]) == len(query)
		except (IndexError, KeyError):
			anagram_found = False

		# remove empty lists
		for key, val in deepcopy(scores).items():
			with suppress(IndexError, KeyError):
				if not val:
					del scores[key]
					if self['debug']:
						print(f' - removed {[key]} for empty list')
				elif not self['noscores'] and any(
					word in scores[key][0] for word in scores[key-1][0]
				):
					del scores[key]
					if self['debug']:
						print(f' - removed {[key]} for duplicate/s')

		# return solved object and anagram status
		return scores, anagram_found

	# solve to string function
	def solve_str(
		self,
		query: str
	):
		'''
		Finds all possible words that can be formed from the given query string, using the set wordlist.

		Args:
			query (`str`): A string representing the query to be solved.

		Returns:
			`str`: A string representing the output of the solver, formatted with headers and indentation.
		'''

		# build query
		query = build_query(query, not self['repeats'])

		# get solved object and anagram status
		scores, anagram_found = self.solve(query)

		# prepare anagram message
		anagram_found = '' if anagram_found else '  \t warning: anagram not found\n\n'

		# return output string
		return str(
			f'\n  \t--- query: {query} ({len(query)} letters'
			+ (' + repeats' if self['repeats'] else '') + ') ---\n\n' + (
				(
					anagram_found + '\n\n'.join(
						f'\t{key} letters'
						+ (
							''
							if self['noscores']
							else f' - {scores[key][1]} points'
						) + '\n\t ' + ', '.join(
							sorted(
								word.lower() if self['lower'] else word.upper()
								for word in scores[key][0]
							)
						)
						for key in scores.keys()
						if scores[key][0]
					)
				)
				if any(scores[key][0] for key in scores.keys())
				else '\t no words found'
			) + '\n'
		)

	# get wordlist
	def get_wordlist(
		self,
		output_type: type = List[str],
	) -> Any:
		'''
		Returns the current wordlist, as defined in the ruleset settings.

		Args:
			`output_type: type`: Type for output to be converted to. Defaults to `list[str]`.

		Returns:
			`Any`: The wordlist, converted to `output_type`.
		'''

		# return wordlist as specified type
		return output_type(self.wordlist)

# entry point
def main():

	# imports
	from jarguments import JArgument, JParser

	# get arguments
	args = JParser(
		*{
			JArgument(arg, type, default, sarg, nargs, help)
			for arg, sarg, type, default, nargs, help in kwargs
		}
	)

	# show message
	with suppress(KeyboardInterrupt):
		print('\n\tloading settings and wordlist..')

		# load settings
		try:
			with open(
				path.join(
					syspath[0], 'qrs.json'
				), 'tr'
			) as settings_file:
				settings_import = load(settings_file)

		# file is empty
		except decoder.JSONDecodeError:
			settings_import = {}

			# display message
			print('\t\'qrs.json\' is empty or invalid; continuing with default/given settings..')

		# file cannot be loaded
		except FileNotFoundError:
			settings_import = {}

			# display message
			print('\tfailed to load \'qrs.json\'; continuing with default/given settings..')

		# load ruleset
		q = Ruleset(
			settings=build_settings(
				{
					**settings_import, **{
						arg: getattr(args, arg)
						for arg, _, _, _, _, _ in kwargs
						if getattr(args, arg, None) is not None
					}
				}
			)
		)

		# save settings
		try:
			with open(
				path.join(
					syspath[0], 'qrs.json'
				), 'tw'
			) as settings_file:
				settings_file.write(
					q.get_settings_str()
				)

		# if settings file cannot be saved
		except Exception:
			print('\tfailed to save \'qrs.json\'; continuing without saving..')

		# debug info
		if (args.debug or q['debug']):
			print(f'\n{q.get_settings_str()}')

		# show message
		print('\n\t\tdone!\n')

		# input loop
		while True:
			query = ''
			while not all([
				q['min'] <= len(query) <= q['max'],
				all(char in ascii_lowercase for char in query)
			]):
				query = input('qrs: ')
			print(q.solve_str(query))

# main function
if __name__ == '__main__':
	main()
