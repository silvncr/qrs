
> Works on Python 3.12.0 and above. Tested on Windows 10.

## Summary

Tool for *Quarrel* by *Denki Games* (released on *iOS* in 2011 and *Xbox Live Arcade* in 2012).

## How to use

Run `main.py`.

```sh
$ python3 main.py
```

The input screen looks like this:

```
> _
```

Type your letters into the field, press <kbd>Enter</kbd>, and wait for the program to calculate the best words. Once it's done, choose one from the list that corresponds with the number of letters you have available, or the next lowest. See the example below to find out why you might not need to use all of your spaces.

### Example case

Here's an example using the default program settings. Our situation is the following:

- We're playing *Quarrel* (thus we can only use words up to 8 letters).
- We have seven (7) spaces.
- Our letters are `wetodlnm`.

We'll input our letters and press <kbd>Enter</kbd>.

```
> wetodlnm

        --- query: delmnotw (8 letters) ---

        8 letters - 18 points
         meltdown

        5 letters - 14 points
         mowed

        4 letters - 12 points
         mewl

        3 letters - 10 points
         mew, mow, wem

        2 letters - 6 points
         ew, ow, we, wo

> _
```

Obviously, we can't make the anagram `MELTDOWN` because we can only use 7 letters. In this case, our best word is `MOWED` (14 points). Based on this output, we also know that unless our opponent has 8 spaces, they cannot score higher than 14.

Note that a word like `LETDOWN` (7 letters) scores the same number of points as `MOWED`. However, `LETDOWN` isn't recognised as a "best word" in this example case. This is because when words are tied for points, the program will choose the word/s with the fewest letters.

The fewer letters your word has, the faster you can write it into your game. This is especially important in *Quarrel*, as the tiebreaker for equal points is input speed.

### Settings

Upon running, the program will automatically generate a `settings.json` file in the root directory. This file contains the program's settings, which can be changed to suit your needs.

| Setting | Default | Purpose | Description |
|:-:|:-:|:-:|:--|
| `all_lowercase` | `false`| Readability | Displays output in lowercase letters. The default setting displays capital letters to mimic the style of word games like *Scrabble* and *Quarrel*. |
| `display_debug` | `false` | Debugging | Shows the program's inner workings whilst calculating. Note that this may negatively affect performance on certain devices or IDEs. |
| `allow_repeats` | `false` | Functionality | Determines whether letters can be used more than once. Change this according to your word game's rules; for example, *Scrabble* tiles can only be used once in a single word, whereas *New York Times*'s *Spelling Bee* allows the reuse of letters. |
| `ignore_scores` | `false` | Functionality | Determines whether point values for words are considered, in which case only the highest-scoring words are displayed. If you don't care about scoring, turn this off to see all words. |

- To change your settings, simply open `settings.json` in a text editor and change any `true` or `false` values. Make sure to save the file once you're done.
- If the settings file is not present in your folder, try running the program. It should create the file.
- After saving your settings, the program will not change if it's already running. Close the program and run it again to use the changed settings.

## References

This project makes use of the following resources:

- [The `scrabble` library](https://github.com/benjamincrom/scrabble)'s word list, adapted from *Collins Scrabble Words (2019)* (source: [*StackExchange*](https://boardgames.stackexchange.com/a/38386))
- *Quarrel*'s letter scoring system, taken directly from in-game (source: [*Wikipedia*](https://en.wikipedia.org/wiki/Quarrel_(video_game)#Scoring))
