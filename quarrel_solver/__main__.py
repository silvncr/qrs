import argparse, contextlib, json, os, string, sys
try:
	from __init__ import build_settings, kwargs, Ruleset
except ImportError:
	from quarrel_solver import build_settings, kwargs, Ruleset

parser = argparse.ArgumentParser()

for arg, type, default, nargs, help in kwargs:
	parser.add_argument(
		f'--{arg}',
		type=type,
		nargs=nargs,
		default=default,
		required=False,
		help=help,
	)

args = parser.parse_args()

with contextlib.suppress(KeyboardInterrupt):
	print('\n\tloading settings and wordlist..')

	try:
		with open(
			os.path.join(
				sys.path[0], 'settings.json'
			), 'tr'
		) as settings_file:
			settings_import = json.load(settings_file)

	except FileNotFoundError:
		settings_import = {}

		print('\tfailed to load \'settings.json\'; continuing with default settings..')

	q = Ruleset(
		settings=build_settings(
			{
				**settings_import, **{
					key: getattr(args, key)
					for key in [arg for arg, _, _, _, _ in kwargs]
					if getattr(args, key) and key != 'settings_path'
				}
			}
		)
	)

	if args.display_debug or q['display_debug']:
		print(f'\n{q.get_settings_str().rstrip()}')

	try:
		open(
			os.path.join(
				sys.path[0], 'settings.json'
			), 'tw'
		).write(
			q.get_settings_str()
		)

	except Exception:
		print('\tfalied to save \'settings.json\'; continuing without saving..')

	print('\n\t\tdone!')

	while True:
		print('')
		query = ''
		while not all([
			q['min_words_len'] <= len(query) <= q['max_words_len'],
			all(char in string.ascii_lowercase for char in query)
		]):
			query = input('> ')
		print(q.solve_str(query))
