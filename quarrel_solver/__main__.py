import contextlib, json, os, string, sys
from quarrel_solver import build_settings, Ruleset

with contextlib.suppress(KeyboardInterrupt):

	print('\n\tloading settings, wordlist..')

	try:
		with open(
			os.path.join(
				sys.path[0], 'settings.json'
			), 'tr'
		) as settings_file:
			settings_import = json.load(settings_file)

	except FileNotFoundError:
		settings_import = {}

		print('\n\tcould not load settings.json! continuing with default settings..')

	q = Ruleset(
		settings=build_settings(settings_import)
	)

	if q['display_debug']:
		print(f'\n{q.get_settings()}\n')

	try:
		open(
			os.path.join(
				sys.path[0], 'settings.json'
			), 'tw'
		).write(
			q.get_settings_str()
		)

	except Exception:
		print('\n\tcould not save settings.json! continuing..')

	print('\n\t\tdone!')

	while True:
		print('')
		query = ''
		while not all([
			q['min_words_len'] <= len(query) <= q['max_words_len'],
			all(char not in string.ascii_lowercase for char in query)
		]):
			print(f'\n{
				q.solve_str(
					''.join(
						sorted(dict.fromkeys(input('> ').lower()))
						if q['allow_repeats']
						else sorted(input('> ').lower())
					)
				)
			}\n')
