<!-- omit from toc -->
# qrs

![version](https://img.shields.io/pypi/v/qrs)
![status](https://img.shields.io/github/actions/workflow/status/silvncr/qrs/python-publish.yml)
![downloads](https://img.shields.io/pypi/dm/qrs)

qrs (kyu-arr-ess) is a tool for *Quarrel* and other word games. It provides word game-related tools that can be configured with custom settings, letter scores, and wordlists. qrs can solve anagrams and find the best words to play based on your letters.

- :snake: Supports Python 3.8 and above. Platform-non-constrained.
- :star: Show your support by leaving a star!

---

## Contents

- [Contents](#contents)
- [The qrs library](#the-qrs-library)
- [Direct execution](#direct-execution)
- [Example case](#example-case)
- [Settings](#settings)

---

## The qrs library

Install the qrs library to use its functionality in your projects.

```sh
python -m pip install --upgrade qrs
```

Here's an example of using the library in the kernel:

<details><summary>Click to expand</summary>

---

> [!IMPORTANT]
> `json.dumps()` converts `int` keys to `str`. You should read `"8": {...}` as `8: {...}`, etc.

```py
>>> import json
>>> from qrs import Ruleset
>>>
>>> rs = Ruleset(max=8)  # load 2-letter to 8-letter words
>>> query = 'wetodlnm'  # query to solve
>>>
>>> solved = rs.solve_query(query)  # solve the query
>>>
>>> if solved.anagram_found:  # check if any anagrams were found; prevents IndexError on next line
...     print(solved.scores[len(query)].words)  # print anagrams as set[str]
{'MELTDOWN'}
>>> print(json.dumps(solved.to_dict(), indent=4))  # full output
{
    "query": "delmnotw",
    "anagram_found": true,
    "scores": {
        "8": {
            "score": 18,
            "words": [
                "MELTDOWN"
            ]
        },
        "5": {
            "score": 14,
            "words": [
                "MOWED"
            ]
        },
        "4": {
            "score": 12,
            "words": [
                "MEWL"
            ]
        },
        "3": {
            "score": 10,
            "words": [
                "MEW",
                "MOW",
                "WEM"
            ]
        },
        "2": {
            "score": 6,
            "words": [
                "OW",
                "WE",
                "EW",
                "WO"
            ]
        }
    }
}
>>> _
```

---

</details>

> [!NOTE]
> The API has changed in version `2.x`. Most code written for `1.x` will not work with `2.x`.
>
> You don't have to update your settings file.
>
> Version `1.x` is still available on PyPI as `qrs==1.*`.

---

## Direct execution

```sh
$ qrs

qrs: _
```

Upon being called from the command line, it will display an input screen.

Enter your letters and wait for the program to calculate the best words. Choose one from the list that corresponds with the number of letters you have available, or the next longest. See the example below to find out why you might not need to use all of your spaces.

---

## Example case

Here's an example using the default program settings. Our situation is the following:

- We're playing *Quarrel*, so we get eight letters.
- Our letters are `wetodlnm`.
- We have seven spaces to use.

After installing the library, we'll open a command line and run the program.

The program will have to load a wordlist, which takes longer as the range of word lengths increases. Since we know we don't need words longer than eight letters, we can minimise loading time by configuring the program to only calculate for words of that length. We can do this by passing our desired settings as command arguments:

```sh
$ qrs --max 8

qrs: _
```

> [!TIP]
> You could instead create a `qrs.json` file, then run the command from the same directory:
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

> [!NOTE]
> A word like `LETDOWN` scores the same number of points as `MOWED`, but isn't recognised as a "best word" in this case. This is because when words are tied for points, the program will choose the word/s with the fewest letters.
>
> The fewer letters your word has, the faster you can write it into your game. This is especially important in *Quarrel*, as the tiebreaker for equal points is input speed.
>
> You can choose to display longer, tied words by enabling the `--doubles` setting.

---

## Settings

Upon being run from the command line, the program will automatically generate (or look for) a `qrs.json` file in the directory from which the command is run. This file contains the program's settings, which can be changed to suit your needs.

When using qrs as a library, pass any of the following args to a `Ruleset` to create a new instance. Here are all the currently supported settings:

| | Setting | Shortcut | Default | Description |
| :-: | :-: | :-: | :-: | :-- |
| :bug: | `debug` | `-d` | `false` | Prints the program's inner workings while calculating. Note that many consecutive print statements may negatively affect performance on certain devices or IDEs. |
| :twisted_rightwards_arrows: | `doubles` | `-b` | `false` | Shows longer words that tie for score (like the `MOWED` / `LETDOWN` example above). |
| :no_entry: | `exclude` | `-e` | `[]` | List of words that the program will never output. |
| :video_game: | `game` | `-g` | `"quarrel"` | Determines the letter scoring system used for calculating points. The value here is passed into `build_letter_scores()`, and defaults back if invalid. |
| :heavy_check_mark: | `include` | `-i` | `[]` | List of additional words for the wordlist. |
| :computer: | `lower` | `-l` | `false` | Displays output in lowercase letters. The default setting displays uppercase letters (in the style of word games like *Quarrel* and *Scrabble*), however some people may find lowercase output more readable. Note that this only affects output; all internal operations are performed in lowercase (wordlist and query storage, etc). |
| :arrow_up_small: | `max` | `-m` | `28` **\*** | Determines the maximum word length the program will calculate for. |
| :arrow_down_small: | `min` | `-n` | `2` | Determines the minimum word length the program will calculate for. |
| :100: | `noscores` | `-s` | `false` | Displays all words, not just those with the highest scores. This will sort by word length. |
| :repeat: | `repeats` | `-r` | `false` | Determines whether letters can be used more than once. Change this according to your word game's rules; for example, *Scrabble* tiles can only be used once in a word, whereas *New York Times Spelling Bee* allows the reuse of letters. |

> [!NOTE]
> **\*** The `max` parameter's default value automatically adjusts to the length of the longest word(s) in the wordlist. For the default wordlist, this is 28. If you use a custom wordlist, this setting will default to the length of the longest word(s) in that list.

When running directly:

- To change your settings, do one of the following:
  - Open `qrs.json` in a text editor and change any values. Make sure to save the file.
  - Pass the setting as a command argument like this: `--setting value`
    - If applicable, this will automatically update the settings file.

```sh
$ qrs --lower --max 8 --debug

  # debug info displayed here (because of --debug flag)

qrs: _
```

- If `qrs.json` is not in your folder, try running the program and letting it fully load. It should then create the file.
- After saving `qrs.json`, the program will not change if it's already running. Close the program and rerun it to use the changed settings.

> [!TIP]
> Every command line argument has a corresponding shortcut. For example, `--lower` can be shortened to `-l`. You can use these shortcuts to save time when entering settings. Here is the previous example with shortcuts:
>
> ```sh
> $ qrs -l -m 8 -d
> ```
>
> If you're unsure about a setting, you can check the program's help message by running `qrs --help`.
>
> ```sh
> $ qrs --help
> ```
>
> Shortcuts and help messages are only available when running the program from the command line.

---

© 2023-2024 silvncr

[MIT License](https://github.com/silvncr/qrs/blob/main/LICENSE)
