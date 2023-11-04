
---

<div align="center">

<h1><code>quarrel-solver</code></h1>

<h3>Tool for <em>Quarrel</em> (and other word games)</h3>

![[publish status](https://github.com/silvncr/quarrel/actions/workflows/python-publish.yml)](https://github.com/silvncr/quarrel/actions/workflows/python-publish.yml/badge.svg)
![[latest release](https://github.com/silvncr/quarrel/releases/latest)](https://img.shields.io/github/v/release/silvncr/quarrel)

</div>

---

## Summary

Provides word game-related tools, and can be configured with custom settings, letter scores, and wordlists.

> Works on Python 3.6 and above. Tested on Windows 10.

---

## Contents


- [Summary](#summary)
- [Contents](#contents)
- [The `quarrel-solver` library](#the-quarrel-solver-library)
- [Direct execution](#direct-execution)
- [Example case](#example-case)
- [Settings](#settings)

---

## The `quarrel-solver` library

Install the `quarrel-solver` library to use all functionality in your own projects.

> Remember to always use the latest version, as not all bugfixes are documented!

```sh
$ py -m pip install --upgrade quarrel-solver
$ py
```

```py
>>> from quarrel_solver import build_settings, Ruleset
>>> q = Ruleset(
...     settings=build_settings(
...         {'max_words_len': 8}
...     )
... )
>>> print(
...     q.solve_str('wetodlnm')
... )

        --- query: delmnotw (8 letters) ---

        8 letters - 18 points
         MELTDOWN

        5 letters - 14 points
         MOWED

        4 letters - 12 points
         MEWL

        3 letters - 10 points
         MEW, MOW, WEM

        2 letters - 6 points
         EW, OW, WE, WO

>>> _
```

> Note: for the `pip install` command, you can use `quarrel-solver` with a hyphen, or `quarrel_solver` with an underscore. When importing the module in Python or running it from the commandline, you **MUST** use an underscore.

For a more informed walkthrough, please see the [example case](#example-case) below.

---

## Direct execution

```sh
$ py -m quarrel_solver
```

If you call the library directly, you'll be greeted with a commandline program. Its input screen looks like this:

```py
> _
```

Type your letters into the field, press <kbd>Enter</kbd>, and wait for the program to calculate the best words. Once it's done, choose one from the list that corresponds with the number of letters you have available, or the next lowest. See the example below to find out why you might not need to use all of your spaces.

---

## Example case

Here's an example using the default program settings. Our situation is the following:

- We're playing *Quarrel*, and thus we get 8 letters.
- Our letters are `wetodlnm`.
- We have 7 spaces to use.

After installing the library, we'll open a commandline and run the program.

Since we know we don't need words longer than 8 letters, we can minimise loading time by configuring the program to only calculate for words of that length. We can do this by passing our desired settings as command arguments:

```sh
$ py -m quarrel_solver --max_words_len 8
```

> Note: this has the same effect as creating a `settings.json` file, then running the command from the same directory:
>
> ```jsonc
> // settings.json
> {"max_words_len": 8}
> ```
>
> ```sh
> ## from folder with settings.json
> $ py -m quarrel_solver
> ```

Whichever way the program is run, it will have to load a wordlist. Once it finishes loading, we can input our letters and press <kbd>Enter</kbd>.

```py
> wetodlnm

        --- query: delmnotw (8 letters) ---

        8 letters - 18 points
         MELTDOWN

        5 letters - 14 points
         MOWED

        4 letters - 12 points
         MEWL

        3 letters - 10 points
         MEW, MOW

        2 letters - 6 points
         OW, WE, WO

> _
```

This tells us that the anagram is `MELTDOWN`, but we can't make that word because we can only use 7 letters. In this case, our best word is `MOWED` (14 points). Based on this output, we also know that our opponent cannot score higher than us without all 8 spaces.

> Note: a word like `LETDOWN` scores the same number of points as `MOWED`, but isn't recognised as a "best word" in this case. This is because when words are tied for points, the program will choose the word/s with the fewest letters.
>
> The fewer letters your word has, the faster you can write it into your game. This is especially important in *Quarrel*, as the tiebreaker for equal points is input speed.

---

## Settings

Upon being run directly, the program will automatically generate (or look for) a `settings.json` file in the directory which the command is run from. This file contains the program's settings, which can be changed to suit your needs.

When using `quarrel-solver`, you should can pass a `dict` with any of the following keys into `build_settings` to generate a full settings object, then pass the output to a `Ruleset` to create a new instance. Here are all the currently supported settings:

| Setting | Default | Description |
|:-:|:-:|:--|
| `all_lowercase` | `false`| Displays output in lowercase letters. The default setting displays capital letters to mimic the style of word games like *Scrabble* and *Quarrel*. However, some people may find lowercase output more readable. |
| `allow_repeats` | `false` | Determines whether letters can be used more than once. Change this according to your word game's rules; for example, *Scrabble* tiles can only be used once in a single word, whereas *New York Times*'s *Spelling Bee* allows the reuse of letters. |
| `display_debug` | `false` | Shows the program's inner workings whilst calculating. Note that this may negatively affect performance on certain devices or IDEs. |
| `exclude_words` | `[]` | List of words that the program will never output. |
| `ignore_scores` | `false` | Determines whether point values for words are considered, in which case only the highest-scoring words are displayed. If you don't care about scoring, turn this off to see all words. |
| `include_words` | `[]` | List of additional words for the wordlist. |
| `letter_scores` | `"quarrel"` | Determines the letter scoring system used for calculating points. The value here is passed into `build_letter_scores()`, and defaults back if invalid. |
| `max_words_len` | longest length in wordlist | Determines the maximum word length the program will calculate for. |
| `min_words_len` | `2` | Determines the minimum word length the program will calculate for. |
| `settings_path`<br>(commandline only) | `None` | Path to the settings file. |

When running directly:

- To change your settings, do one of the following:
  - Open `settings.json` in a text editor and change any values. Make sure to save the file once you're done.
  - Pass the setting as a command argument like this: `--setting_name value`
    - This will automatically update the settings file, if applicable.

```sh
$ py -m quarrel_solver --display_debug true --max_words_len 8
```

- If `settings.json` is not present in your folder, try running the program and letting it fully load. It should then create the file.
- After saving `settings.json`, the program will not change if it's already running. Close the program and run it again to use the changed settings.

---
