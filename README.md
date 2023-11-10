
---

<div align="center">

<h1><code>pip install qrs</code></h1>

<h3>Tool for <em>Quarrel</em> (and other word games)</h3>

![[publish status](https://github.com/silvncr/qrs/actions/workflows/python-publish.yml)](https://github.com/silvncr/qrs/actions/workflows/python-publish.yml/badge.svg)
![[latest release](https://github.com/silvncr/qrs/releases/latest)](https://img.shields.io/github/v/release/silvncr/qrs)

</div>

---

## Summary

Provides word game-related tools, and can be configured with custom settings, letter scores, and wordlists.

> Works on Python 3.9 and above. Tested on Windows 10.

---

## Contents

- [Summary](#summary)
- [Contents](#contents)
- [The `qrs` library](#the-qrs-library)
- [Direct execution](#direct-execution)
- [Example case](#example-case)
- [Settings](#settings)

---

## The `qrs` library

Install the `qrs` library to use all functionality in your own projects.

```sh
$ py -m pip install --upgrade qrs
$ py
```

```py
>>> from qrs import build_settings, Ruleset
>>> q = Ruleset(
...     build_settings(
...         {'max': 8}
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

---

## Direct execution

```sh
$ py -m qrs
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
$ py -m qrs --max 8
```

> Note: this has the same effect as creating a `settings.json` file, then running the command from the same directory:
>
> ```jsonc
> // settings.json
> {"max": 8}
> ```
>
> ```sh
> ## from folder with settings.json
> $ py -m qrs
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

When using `qrs`, you should can pass a `dict` with any of the following keys into `build_settings` to generate a full settings object, then pass the output to a `Ruleset` to create a new instance. Here are all the currently supported settings:

| Setting | Default | Description |
|:-:|:-:|:--|
| `debug` | `false` | Shows the program's inner workings whilst calculating. Note that this may negatively affect performance on certain devices or IDEs. |
| `exclude` | `[]` | List of words that the program will never output. |
| `game` | `"quarrel"` | Determines the letter scoring system used for calculating points. The value here is passed into `build_letter_scores()`, and defaults back if invalid. |
| `include` | `[]` | List of additional words for the wordlist. |
| `lower` | `false`| Displays output in lowercase letters. The default setting displays capital letters to mimic the style of word games like *Scrabble* and *Quarrel*, however some people may find lowercase output more readable. |
| `max` | longest length in wordlist | Determines the maximum word length the program will calculate for. |
| `min` | `2` | Determines the minimum word length the program will calculate for. |
| `noscores` | `false` | Determines whether point values for words are considered, in which case only the highest-scoring words are displayed. If you don't care about scoring, turn this on to see all words. |
| `repeats` | `false` | Determines whether letters can be used more than once. Change this according to your word game's rules; for example, *Scrabble* tiles can only be used once in a single word, whereas *New York Times*'s *Spelling Bee* allows the reuse of letters. |

When running directly:

- To change your settings, do one of the following:
  - Open `settings.json` in a text editor and change any values. Make sure to save the file once you're done.
  - Pass the setting as a command argument like this: `--setting value`
    - This will automatically update the settings file, if applicable.

```sh
$ py -m qrs --lower --max 8 --debug
```

- If `settings.json` is not present in your folder, try running the program and letting it fully load. It should then create the file.
- After saving `settings.json`, the program will not change if it's already running. Close the program and run it again to use the changed settings.

---
