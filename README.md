<!-- omit from toc -->
# qrs

tool for *Quarrel* (and other word games)

![version](https://img.shields.io/pypi/v/qrs)
![status](https://img.shields.io/github/actions/workflow/status/silvncr/qrs/python-publish.yml)
![downloads](https://img.shields.io/pypi/dm/qrs)

## Summary

Provides word game-related tools that can be configured with custom settings, letter scores, and wordlists.

- :snake: Supports Python 3.8 and above. Tested on Windows 10.
- :star: Show your support by leaving a star!

## Contents

- [Summary](#summary)
- [Contents](#contents)
- [The qrs library](#the-qrs-library)
- [Direct execution](#direct-execution)
- [Example case](#example-case)
- [Settings](#settings)

## The qrs library

Install the qrs library to use its functionality in your projects.

```sh
python -m pip install --upgrade qrs
```

```py
>>> from qrs import Ruleset
>>> q = Ruleset({'max': 8})
>>> print(q.solve_str('wetodlnm'))

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

## Direct execution

```sh
$ qrs

qrs: _
```

Upon being called from the command line, it will display an input screen.

Enter your letters and wait for the program to calculate the best words. Choose one from the list that corresponds with the number of letters you have available, or the next longest. See the example below to find out why you might not need to use all of your spaces.

## Example case

Here's an example using the default program settings. Our situation is the following:

- We're playing *Quarrel*, and thus, we get eight letters.
- Our letters are `wetodlnm`.
- We have seven spaces to use.

After installing the library, we'll open a command line and run the program.

The program will have to load a wordlist, which takes longer as the range of word lengths increases. Since we know we don't need words longer than eight letters, we can minimise loading time by configuring the program to only calculate for words of that length. We can do this by passing our desired settings as command arguments:

```sh
$ qrs --max 8

qrs: _
```

> Note: this has the same effect as creating a `qrs.json` file, then running the command from the same directory:
>
> ```jsonc
> // qrs.json
> {"max": 8}
> ```
>
> ```sh
> ## from folder with qrs.json
> $ qrs
> ```

Once it finishes loading, we can enter our letters.

```py
qrs: wetodlnm

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

qrs: _
```

This output tells us that the anagram is `MELTDOWN`, but we can't make that word because we can only use seven letters. In this case, our best word is `MOWED` (14 points). Based on this output, we also know that our opponent cannot score higher than us without all eight spaces.

> Note: a word like `LETDOWN` scores the same number of points as `MOWED`, but isn't recognised as a "best word" in this case. This is because when words are tied for points, the program will choose the word/s with the fewest letters.
>
> The fewer letters your word has, the faster you can write it into your game. This is especially important in *Quarrel*, as the tiebreaker for equal points is input speed.
>
> You can choose to display longer, tied words by enabling the `--doubles` setting.

## Settings

Upon being run from the command line, the program will automatically generate (or look for) a `qrs.json` file in the directory from which the command is run. This file contains the program's settings, which can be changed to suit your needs.

When using qrs as a library, pass a `dict` with any of the following keys to a `Ruleset` to create a new instance. Here are all the currently supported settings:

| Setting | Default | Description |
| :-: | :-: | :-- |
| `debug` 🐛 | `false` | Prints the program's inner workings whilst calculating. Note that many consecutive print statements may negatively affect performance on certain devices or IDEs. |
| `doubles` 🔀 | `false` | Shows longer words that tie for score (like the `MOWED` / `LETDOWN` example above). |
| `exclude` ⛔ | `[]` | List of words that the program will never output. |
| `game` 🎮 | `"quarrel"` | Determines the letter scoring system used for calculating points. The value here is passed into `build_letter_scores()`, and defaults back if invalid. |
| `include` ✔️ | `[]` | List of additional words for the wordlist. |
| `lower` 💻 | `false` | Displays output in lowercase letters. The default setting displays capital letters to mimic the style of word games like *Scrabble* and *Quarrel*, however some people may find lowercase output more readable. |
| `max` 🔼 | longest length in wordlist | Determines the maximum word length the program will calculate for. |
| `min` 🔽 | `2` | Determines the minimum word length the program will calculate for. |
| `noscores` 💯 | `false` | Determines whether point values for words are considered, in which case only the highest-scoring words are displayed. If you don't care about scoring, turn this on to see all words. |
| `repeats` 🔁 | `false` | Determines whether letters can be used more than once. Change this according to your word game's rules; for example, *Scrabble* tiles can only be used once in a word, whereas *New York Times*'s *Spelling Bee* allows the reuse of letters. |

When running directly:

- To change your settings, do one of the following:
  - Open `qrs.json` in a text editor and change any values. Make sure to save the file once you're done.
  - Pass the setting as a command argument like this: `--setting value`
    - If applicable, this will automatically update the settings file.

```sh
$ qrs --lower --max 8 --debug

  # debug info displayed here

qrs: _
```

- If `qrs.json` is not in your folder, try running the program and letting it fully load. It should then create the file.
- After saving `qrs.json`, the program will not change if it's already running. Close the program and rerun it to use the changed settings.
