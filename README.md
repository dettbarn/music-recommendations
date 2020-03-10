# music-recommendations

From the user's favorite musical artists, generate a set of recommendations.

## Introduction

It is planned to use several different APIs and online databases. But currently, only the last.fm API is supported.

## Installation and usage

* Paste your last.fm API key into a file named `.api_key` in the `lastfm` subfolder.
* Write a set of musical artists, one artist per line, into a file named `input.txt` in the root folder, together with a weighting factor, delimited by a `%` character, e.g.:
  ```
  The Beatles%3
  Radiohead%2
  Muse%1.5
  ```
  Note that the software works the better, the more artists and reasonable weighting factors you supply.
* Run `python musicrecs.py`.
* Recommendations for you are written into `output.txt` together with weighting factors. If you would like to know why certain artists are recommended to you, you can look into `outroot.txt` to find out.
