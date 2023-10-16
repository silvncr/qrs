import contextlib, copy, json, os, scrabble, string, sys

with contextlib.suppress(KeyboardInterrupt):
	letters = {
		"a": 1, "b": 5, "c": 2, "d": 3, "e": 1, "f": 5, "g": 4,
		"h": 4, "i": 1, "j": 15, "k": 6, "l": 2, "m": 4, "n": 1,
		"o": 1, "p": 3, "q": 15, "r": 2, "s": 1, "t": 1, "u": 3,
		"v": 6, "w": 5, "x": 10, "y": 5, "z": 12
	}
	scores = {
		word: sum(letters[char] for char in word) for word in sorted(
			sorted(scrabble.scrabble.config.ENGLISH_DICTIONARY_SET),
			key=lambda word: (
				len(word), sum(letters[char] for char in word)
			), reverse=True
		)
	}
	try:
		with open(
			os.path.join(
				sys.path[0], 'settings.json'
			), 'tr'
		) as settings_file:
			settings_import = json.load(settings_file)

	except FileNotFoundError:
		settings_import = {}

	settings = {
		s: False for s in [
			'all_lowercase',
			'display_debug',
			'allow_repeats',
			'ignore_scores',
		]
	} | settings_import
	open(
		os.path.join(
			sys.path[0], 'settings.json'
		), 'tw'
	).write(
		json.dumps(settings, indent=2).replace('  ', '\t')
	)

	del letters, settings_import

	while True:
		print('')
		in_str = ''
		while not 2 <= len(in_str) <= max(
			len(word) for word in scrabble.scrabble.config.ENGLISH_DICTIONARY_SET
		) and (
			char not in string.ascii_lowercase for char in in_str
		):
			in_str = ''.join(
				sorted(dict.fromkeys(input('> ').lower()))
				if settings['allow_repeats']
				else sorted(input('> ').lower())
			)

		scores_out = {}

		if settings['display_debug']:
			print('')

		for len_iter in range(
			2, max(
				len(word) for word in scrabble.scrabble.config.ENGLISH_DICTIONARY_SET
			) if settings['allow_repeats'] else len(in_str) + 1
		)[::-1]:
			scores_out |= {len_iter: [[], 0]}
			for word in scores:
				in_str_iter, word_iter = copy.deepcopy(in_str), copy.deepcopy(word)
				word_fits = False

				if (
					len(word) == len_iter
					if settings['ignore_scores']
					else len(word) <= len_iter
				) and set(word) <= set(in_str):
					if not settings['ignore_scores'] and scores[word] < scores_out[len_iter][1]:
						continue

					if settings['allow_repeats']:
						word_fits = all(char in in_str for char in word)

					else:
						for char in word:
							in_str_iter = in_str_iter.replace(char, ' ', 1)
							word_iter = word_iter.replace(char, ' ', 1)

							if settings['display_debug']:
								print(f'input: {[in_str_iter]} | {[word]}: {[word_iter]}')

						if in_str_iter.count(' ') == word_iter.count(' ') != 0:
							word_fits = True

					if settings['display_debug']:
						print(f'{[word]} fits for {[len_iter]}')

				if word_fits:
					scores_out[len_iter][0].append(word)
					if not settings['ignore_scores']:
						scores_out[len_iter][1] = scores[scores_out[len_iter][0][0]]

			if settings['display_debug']:
				print(f' - output for {[len_iter]}: {scores_out[len_iter][0]}')

		try:
			if len(scores_out[len(in_str)][0][0]) != len(in_str):
				anagram_found = '  \t warning: anagram not found\n\n'
			else:
				anagram_found = ''
		except (IndexError, KeyError):
			anagram_found = ''

		for key, val in copy.deepcopy(scores_out).items():
			with contextlib.suppress(IndexError, KeyError):
				if not val:
					del scores_out[key]
					if settings['display_debug']:
						print(f' - removed {[key]} for empty list')
				elif not settings['ignore_scores'] and any(
					word in scores_out[key][0] for word in scores_out[key-1][0]
				):
					del scores_out[key]
					if settings['display_debug']:
						print(f' - removed {[key]} for duplicate/s')

		print(
			f'\n  \t--- query: {in_str} ({len(in_str)} letters'
			+ (' + repeats' if settings['allow_repeats'] else '') + ') ---\n\n' + (
				(
					anagram_found + '\n\n'.join(
						f'\t{key} letters'
						+ (
							''
							if settings['ignore_scores']
							else f' - {scores_out[key][1]} points'
						) + '\n\t ' + ', '.join(
							sorted(
								word if settings['all_lowercase'] else word.upper()
								for word in scores_out[key][0]
							)
						)
						for key in scores_out.keys()
						if scores_out[key][0]
					)
				)
				if any(scores_out[key][0] for key in scores_out.keys())
				else '\tno words found'
			)
		)
