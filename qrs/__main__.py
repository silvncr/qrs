# imports
from contextlib import suppress
from json import decoder, load
from os import path
from string import ascii_lowercase
from sys import exit, path as syspath

# import from self
try:
	from .__init__ import BooleanAction, build_settings, kwargs, parser, Ruleset
except ImportError:
	print('\n\tcould not import from self; falling back to file..')
	try:
		from __init__ import BooleanAction, build_settings, kwargs, parser, Ruleset
	except ImportError:
		print('\tcould not import from file; falling back to library..')
		try:
			from qrs import BooleanAction, build_settings, kwargs, parser, Ruleset
		except ImportError:
			input('\n\tfallbacks failed; now aborting. press enter to exit.')
			exit()

# set arguments
for arg, sarg, type, default, nargs, help in kwargs:
	if type == bool:
		parser.add_argument(
			f'--{arg}',
			f'-{sarg}',
			dest=arg,
			action=BooleanAction,
			default=None,
			help=help
		)
	else:
		parser.add_argument(
			f'--{arg}',
			f'-{sarg}',
			type=type,
			nargs=nargs,
			default=default,
			required=False,
			help=help,
		)

# get arguments
args = parser.parse_args()

# show message
with suppress(KeyboardInterrupt):
	print('\n\tloading settings and wordlist..')

	# load settings
	try:
		with open(
			path.join(
				syspath[0], 'settings.json'
			), 'tr'
		) as settings_file:
			settings_import = load(settings_file)

	# file is empty
	except decoder.JSONDecodeError:
		settings_import = {}

		# display message
		print('\t\'settings.json\' is empty or invalid; continuing with default/given settings..')

	# file cannot be loaded
	except FileNotFoundError:
		settings_import = {}

		# display message
		print('\tfailed to load \'settings.json\'; continuing with default/given settings..')

	# load ruleset
	q = Ruleset(
		settings=build_settings(
			settings_import | {
				arg: getattr(args, arg)
				for arg, _, _, _, _, _ in kwargs
				if getattr(args, arg) is not None
			}
		)
	)

	# debug info
	if (args.debug or q['debug']):
		print(f'\ncurrent settings: {q.get_settings_str()}')

	# save settings
	try:
		with open(
			path.join(
				syspath[0], 'settings.json'
			), 'tw'
		) as settings_file:
			settings_file.write(
				q.get_settings_str()
			)

	# if settings file cannot be saved
	except Exception:
		print('\tfailed to save \'settings.json\'; continuing without saving..')

	# show message
	print('\n\t\tdone!\n')

	# input loop
	while True:
		query = ''
		while not all([
			q['min'] <= len(query) <= q['max'],
			all(char in ascii_lowercase for char in query)
		]):
			query = input('> ')
		print(q.solve_str(query))
