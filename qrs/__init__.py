'''
Provides word game-related tools that can be configured with custom settings,
letter scores, and wordlists.
'''

from __future__ import annotations

__author__ = 'silvncr'
__license__ = 'MIT'
__module__ = 'qrs'
__version__ = '2.0.1'


from contextlib import suppress
from copy import deepcopy
from json import dumps, load
from json.decoder import JSONDecodeError
from os import path as os_path
from string import ascii_lowercase
from sys import path as sys_path
from typing import Any, ClassVar, Set

# get full wordlist from file
with open(
	os_path.join(
		os_path.dirname(__file__),
		'wordlist.txt',
	),
) as f:
	wordlist_full: set[str] = set(f.read().splitlines())
max_length_full: int = max(len(word) for word in wordlist_full)


# get letter scores for name
def build_letter_scores(
	name: str | None = None,
	/,
) -> dict[str, int]:
	'''
	Returns the letter scores for the given name. To be passed into the
	`Ruleset` class.

	Args:
	----
		name: `str` (optional)
			The name of the letter scoring system.
			Defaults to *Quarrel*.

	Returns:
	-------
		`dict[str, int]`
			A dictionary of letter scores, with letters as keys and scores
			as values, or an empty dictionary if `name` is invalid.
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
					'v': 6, 'w': 5, 'x': 10, 'y': 5, 'z': 12,
				},
				'scrabble': {
					'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
					'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
					'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
					'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,
				},
			}.items()
			if name == key
		), {},
	)


# get query string
def build_query(
	query: str,
	/,
	*,
	repeat_letters: bool = True,
) -> str:
	'''
	Returns a sorted query string, with optional repeats.

	Args:
	----
		query: `str`
			Query string to sort.
		repeat_letters: `bool` (optional)
			Whether to allow repeating letters in the query string.
			Usually the *opposite* of `Ruleset()['repeats']`.
			Defaults to True.

	Returns:
	-------
		`str`: The inputted query string, but sorted.
	'''
	return ''.join(
		sorted(query.lower())
		if repeat_letters
		else sorted(set(dict.fromkeys(query.lower()))),
	).lower()


# get settings object from settings
def build_settings(
	user_settings: dict[str, Any] | None = None,
	wordlist: set[str] | None = None,
	/,
) -> dict[str, Any]:
	'''
	Returns the settings for the given user settings.

	Args:
	----
		user_settings: `dict[str, Any]` (optional)
			Custom settings to override the default settings.
			Defaults to an empty dictionary.
		wordlist: `set[str]` (optional)
			Wordlist used to determine defaults for word-related settings.
			Defaults to the *Collins Scrabble Dictionary (2019)*,
			which is the only built-in wordlist.

	Returns:
	-------
		`dict[str, Any]`: A dictionary of settings.
	'''

	# user_settings default
	if not user_settings:
		user_settings = {}

	# wordlist default
	_wordlist = wordlist or wordlist_full

	# remove excluded words
	if 'exclude' in user_settings:
		for word in user_settings['exclude']:
			if (word) and (word in _wordlist):
				_wordlist.remove(word)

	# add included words
	if 'include' in user_settings:
		for word in user_settings['include']:
			if (word) and (word not in _wordlist):
				_wordlist.add(word)

	# build defaults and determine min-max
	settings = {
		**{
			str(arg): default
			for arg, _, _, default, *_ in Ruleset.qrs_kwargs
		},
		**user_settings,
		'min': max(user_settings['min'], 2) if 'min' in user_settings else 2,
		'max': min(user_settings['max'], max(len(word) for word in _wordlist))
			if 'max' in user_settings
			else max(len(word) for word in _wordlist),
	}

	# set game
	return {
		**settings,
		'game': str(
			settings['game']
			if build_letter_scores(settings['game'])
			else 'quarrel',
		),
	}


# word game ruleset class
class Ruleset:
	'Defines a word game ruleset with custom settings and wordlist.'

	# command line arguments; (arg, sarg, type, default, multiple, help)
	qrs_kwargs: ClassVar[list[tuple]] = [
		('debug', 'd', bool, False, ..., 'Whether to display debug information'),
		('doubles', 'b', bool, False, ..., 'Whether to show longer, tied words'),
		('exclude', 'e', str, [], True, 'List of words to exclude'),
		('game', 'g', str, 'quarrel', None, 'Scoring system to use'),
		('include', 'i', str, [], True, 'List of words to include'),
		('lower', 'l', bool, False, ..., 'Whether output should be lowercase'),
		('max', 'm', int, max_length_full, None, 'Maximum length of words'),
		('min', 'n', int, 2, None, 'Minimum length of words'),
		('noscores', 's', bool, False, ..., 'Whether to ignore scores'),
		('repeats', 'r', bool, False, ..., 'Whether letters can repeat'),
	]

	class Settings:
		'Defines the settings for a ruleset.'

		def __init__(
			self: Ruleset.Settings,
			/,
			**settings: ...,
		) -> None:
			'Initialises the settings.'

			# settings default
			settings = settings or {}

			# update settings
			for key, value in settings.items():
				if any(
					key == _name and isinstance(value, _type)
					for _name, _type in [
						(_arg, _type)
						for _arg, _, _type, *_ in Ruleset.qrs_kwargs
					]
				):
					setattr(self, key, value)

		def __dict__(
			self: Ruleset.Settings,
			/,
		) -> dict[str, Any]:
			'Returns the settings as a dictionary.'

			return {
				_key: getattr(self, _key, None)
				for _key, _, _type, *_ in Ruleset.qrs_kwargs
				if isinstance(getattr(self, _key, None), _type)
			}

		def __getitem__(
			self: Ruleset.Settings,
			name: str,
			/,
		) -> ...:
			'Gets the value of the given setting.'

			return getattr(self, name)

	def __init__(
		self: Ruleset, /, *, wordlist: set[str] | None = None, **settings: ...,
	) -> None:
		'''
		Defines a word game ruleset with the given settings and wordlist.

		Args:
		----
			settings: `dict[str, Any]` (optional)
				Custom settings to override the default settings.
			wordlist: `set[str]` (optional)
				A list of words to be used in the ruleset.
				Defaults to the default wordlist, decided in `build_settings()`.

		Returns:
		-------
			A `Ruleset` with the specified settings and wordlist.
		'''

		# settings default
		_settings = settings or {}

		# wordlist default
		_wordlist = wordlist or wordlist_full

		# remove excluded words
		_wordlist -= set(_settings.get('exclude', []))

		# add included words
		_wordlist |= set(_settings.get('include', []))

		# fix wordlist case
		_wordlist = {word.lower() for word in _wordlist}

		# get settings
		_settings = build_settings(_settings, _wordlist)

		# adjust wordlist to settings
		_wordlist = {
			word for word in _wordlist
			if _settings['min'] <= len(word) <= _settings['max']
		}

		# set settings
		self.settings: Ruleset.Settings = Ruleset.Settings(**_settings)

		# set scores (uses self.__getitem__; self.settings must be defined before)
		self.scores: dict[str, int] = {
			word: sum(
				build_letter_scores(self['game'])
					.get(char, 0)
				for char in word
			)
			for word in sorted(
				_wordlist, key=lambda word: (
					len(word), sum(
						build_letter_scores(self['game']).get(char, 0)
						for char in word
					),
				), reverse=True,
			)
		}

		# set wordlist
		self.wordlist: set[str] = _wordlist

	# getitem method
	def __getitem__(
			self: Ruleset,
			name: str,
			/,
		) -> ...:
		'''
		Returns the value of the given setting, as defined in the ruleset's
		settings.

		Args:
		----
			name: `str`
				The setting to get the value of.

		Returns:
		-------
			The value of the given setting. Can be any type, as defined in
			`qrs._kwargs`.
		'''

		# check for valid setting name
		if any(name == arg for arg, *_ in Ruleset.qrs_kwargs):

			# return setting, or raise error
			if hasattr(self.settings, name):
				return getattr(self.settings, name)

			# raise error
			msg = f'{name!s} not found in settings'
			raise KeyError(msg)

		# raise error
		msg = f'invalid setting: {name!s}'
		raise KeyError(msg)


	# repr method
	def __repr__(self: Ruleset) -> str:
		'Returns a string representation of the ruleset.'
		return f'{self.__class__.__name__}({self.settings!r})'

	# setattr method
	def __setitem__(self: Ruleset, name: str, value: ...) -> None:
		'''
		Sets the value of the given setting.

		Args:
		----
			name: `str`
				The setting to set the value of.
			value: `Any`
				The value to set the setting to.
		'''
		setattr(self.settings, name, value)

	# get settings
	def get_settings(
		self: Ruleset,
		/,
	) -> dict[str, Any]:
		'Returns the current settings as a dictionary.'

		# convert Settings object to dict
		return self.settings.__dict__()

	# return object
	class SolvedQuery:
		'Provides a return object for the `Ruleset().solve_query` method.'

		def __init__(
			self: Ruleset.SolvedQuery,
			/,
			query: str,
			scores: dict[int, Ruleset.LengthInfo],
			*,
			anagram_found: bool,
		) -> None:
			'Initialises the return object.'

			self.query: str = query
			self.scores: dict[int, Ruleset.LengthInfo] = scores
			self.anagram_found: bool = anagram_found

		def to_dict(
			self: Ruleset.SolvedQuery, /,
		) -> dict[str, bool | str | dict[int, dict[str, int | list[str]]]]:
			'Returns the object as a hashable dictionary.'

			return {
				'query': self.query,
				'anagram_found': self.anagram_found,
				'scores': {
					key: {'score': val.score, 'words': list(val.words)}
					for key, val in self.scores.items()
				},
			}

	# info for one word length
	class LengthInfo:
		'Holds one word length and its corresponding data.'

		def __init__(
			self: Ruleset.LengthInfo,
			/,
			length: int,
			score: int,
			words: set[str],
		) -> None:
			'Initialises the object.'

			self.length: int = length
			self.score: int = score
			self.words: set[str] = words

	# solve function
	def solve_query(
		self: Ruleset,
		query: str,
		/,
	) -> SolvedQuery:
		'''
		Finds all possible words that can be formed from the given query
		string using the set wordlist.

		Args:
		----
			query: `str`
				A string representing the query to be solved.

		Returns:
		-------
			`SolvedQuery`:
				An object containing the output. See `SolvedQuery` for more information.
		'''

		# build query
		query = build_query(query, repeat_letters=not self['repeats'])

		# initialise output object
		scores: dict[int, dict[str, int | set[str]]] = {}

		# prepare debug output
		if self['debug']:
			print()

		# iterate through possible word lengths
		for len_iter in range(
			max(2, min([2, self['min']])),
			(self['max'] if self['repeats'] else len(query)) + 1,
		)[::-1]:
			scores[len_iter] = {
				'score': 0,
				'words': set(),
			}

			# iterate through wordlist
			for word in self.scores:
				query_iter, word_iter = deepcopy(query), deepcopy(word)
				word_fits = False

				# handle noscores
				if (
					len(word) == len_iter
					if self['noscores']
					else len(word) <= len_iter
				) and set(word) <= set(query):
					if (
						not self['noscores']
						and self.scores[word] < scores[len_iter]['score']  # type: ignore
					):
						continue

					# handle repeats
					if self['repeats']:
						word_fits = all(char in query for char in word)

					# handle no repeats
					else:
						if self['debug']:
							print(f' - checking [{word}]')

						# iterate through word characters
						for char in word:
							query_iter = query_iter.replace(char, ' ', 1)
							word_iter = word_iter.replace(char, ' ', 1)

						# check if word length is correct
						_length_fits = len(word) == len_iter

						# check if word fits query
						_spaces_fit = query_iter.count(' ') != 0 \
								and query_iter.count(' ') == word_iter.count(' ')

						# check if word fits doubles criteria
						if self['doubles']:
							_doubles_fits = True
						else:
							_doubles_fits = query_iter.count(' ') == \
									word_iter.count(' ') != 0

						# debug info
						if self['debug']:
							print(f'\t{[_length_fits, _spaces_fit, _doubles_fits]}')

						# check if word fits
						if all([
							_length_fits,
							_spaces_fit,
							_doubles_fits,
						]):
							word_fits = True


				# add word to output
				if word_fits:
					scores[len_iter]['words'].add(word)  # type: ignore

					# debug info
					if self['debug']:
						print(
							f'\tinput: [{query_iter}] |',
							f'[{word}]: [{word_iter}]',
						)
						print(f'\t[{word}] fits for [{len_iter}]')
						if not word_iter.strip() and not query_iter.strip() \
								and len(word) == len(query):
							print(f'\tanagram found: [{word}]')

					# update score
					if not self['noscores']:
						scores[len_iter]['score'] = self.scores[
							next(iter(scores[len_iter]['words'])).lower()  # type: ignore
						]

			# debug info
			if self['debug']:
				print(f'output for [{len_iter}]: {scores[len_iter]["words"]}')

		# determine whether an anagram was found
		try:
			anagram_found = len(next(iter(scores[len(query)]['words']))) == len(query)  # type: ignore
		except (IndexError, KeyError, StopIteration):
			anagram_found = False

		# remove empty or non-compliant lists
		for key, val in deepcopy(scores).items():
			with suppress(IndexError, KeyError):
				if not val:
					del scores[key]
					if self['debug']:
						print(f' - removed [{key}] for empty list')
					continue
				if not self['noscores'] and any(
					word in scores[key]['words'] for word in scores[key - 1]['words']  # type: ignore
				):
					del scores[key]
					if self['debug']:
						print(f' - removed [{key}] for duplicate/s')
					continue
				if not self['doubles']:
					_break = False
					for _key in scores:
						if _key < key and any(
							self.scores[word] <= self.scores[_word]
							for word in scores[key]['words']  # type: ignore
							for _word in scores[_key]['words']  # type: ignore
						):
							del scores[key]
							if self['debug']:
								print(f' - removed [{key}] for doubles')
							_break = True
							break
					if _break:
						continue
				if self['debug']:
					print(f' - kept [{key}]')

		# return solved object and anagram status
		return self.SolvedQuery(
			query=query,
			scores={
				key: self.LengthInfo(
					length=key,
					score=val['score'],  # type: ignore
					words = set(  # noqa: C401; using {} makes a generator
						word.lower() if self['lower'] else word.upper()
						for word in val['words']  # type: ignore
					),
				)
				for key, val in scores.items()
			},
			anagram_found=anagram_found,
		)

	# get wordlist
	def get_wordlist(
		self: Ruleset,
		/,
	) -> set[str]:
		'''
		Returns the current wordlist, as defined in the ruleset settings.

		Args:
		----
			output_type: `type`
				Type for output to be converted to.
				Defaults to `set[str]`.

		Returns:
		-------
			`Any`: The wordlist, converted to `output_type`.
		'''

		# get wordlist
		return self.wordlist


# entrypoint
def main() -> None:
	'''
	Provides the functionality for the entrypoint function.

	```sh
	$ qrs
	```

	Not intended to be used within scripts, except in this library's `__main__.py`.
	'''

	# load status
	ready_for_input = False

	# get arguments
	from jarguments import JArgument, JParser
	cmd_args = JParser(
		*{
			JArgument(
				name=arg,
				type=arg_type,
				default=None,
				short_name=sarg,
				multiple=nargs,
				help=arg_help,
			) for arg, sarg, arg_type, _, nargs, arg_help in Ruleset.qrs_kwargs
		},
	)

	# show message
	with suppress(KeyboardInterrupt):
		print('\n\tloading settings and wordlist..')

		# load settings
		try:
			with open(
				os_path.join(
					sys_path[0], 'qrs.json',
				), 'tr',
			) as settings_file:
				settings_import = load(settings_file)

		# file is empty
		except JSONDecodeError:
			settings_import = {}

			# display message
			print(
				'\t\'qrs.json\' is empty or invalid;',
				'continuing with default/given settings..',
			)

		# file cannot be loaded
		except FileNotFoundError:
			settings_import = {}

			# display message
			print(
				'\tcould not find \'qrs.json\';',
				'continuing with default/given settings..',
			)

		# load ruleset
		q = Ruleset(
			**{
				**settings_import, **{
					arg: getattr(cmd_args, arg)
					for arg, *_ in Ruleset.qrs_kwargs
					if getattr(cmd_args, arg, None) is not None
					and arg in [name for name, *_ in Ruleset.qrs_kwargs]
				},
			},
		)

		# save settings
		try:
			with open(
				os_path.join(
					sys_path[0], 'qrs.json',
				), 'tw',
			) as settings_file:
				settings_file.write(
					settings_str := dumps(
						q.settings.__dict__(), indent=2, sort_keys=True,
					).replace('  ', '\t')
					+ '\n',
				)

		# if settings file cannot be saved
		except OSError:
			print(
				'\tfailed to save \'qrs.json\';',
				'continuing without saving..',
			)

		print()

		# debug info
		if (cmd_args.debug or q['debug']):
			print(f'{settings_str}')

		# prepare for input
		ready_for_input = True
		print('\t\tdone!\n')

		# input loop
		while True:
			query = ''
			while not all([
				q['min'] <= len(query) <= q['max'],
				all(char in ascii_lowercase for char in query.lower()),
			]):
				query = input('qrs: ')

			# get solved object and anagram status
			s = q.solve_query(query)

			# prepare anagram message
			anagram_msg = '' \
				if s.anagram_found \
				else '  \t warning: anagram not found\n\n'

			# output formatted string
			print(
				f'\n  \t--- query: {s.query} ({len(query)} letters'
				+ (' + repeats' if q.settings['repeats'] else '') + ') ---\n\n' + (
					(
						anagram_msg + '\n\n'.join(
							f'\t{key} letters'
							+ (
								''
								if q['noscores']
								else f' - {s.scores[key].score} points'  # type: ignore
							) + '\n\t ' + ', '.join(
								sorted(
									word for word in s.scores[key].words  # type: ignore
								),
							)
							for key in s.scores  # type: ignore
							if s.scores[key].words  # type: ignore
						)
					)
					if any(s.scores[key].words for key in s.scores)  # type: ignore
					else '\t no words found'
				) + '\n',
			)

	# pretty exit
	print(
		'\n' if ready_for_input else '',
		'\n\texiting..',
	)


# main function
if __name__ == '__main__':
	main()
