# music-recommendations

From the user's favorite musical artists, generate a set of recommendations.

## Introduction

It is planned to use several different APIs and online databases. But currently, only the last.fm API is supported.

## Installation

Paste your last.fm API key into a file named `.api_key` in the `lastfm` subfolder and you're ready to go.

## Usage

You need a list of your favorite musical artists, one artist per line, together with weighting factors, delimited by a `%` character, e.g.:
```
The Beatles%3
Radiohead%2
Muse%1.5
```

Note that the software works the better, the more artists and reasonable weighting factors you supply.

1. Interactive mode

* Run `python musicrecs.py -i`.
* Enter your list.

2. Input file mode

* Write your list into a file named `input.txt` in the root folder.  
* Run `python musicrecs.py`.

In both cases, recommendations for you will be written into `output.txt` together with weighting factors. If you would like to know why certain artists are recommended to you, you can look into `outroot.txt` to find out.

## Contribute

Everyone can contribute to this project. Take a look at [CONTRIBUTING.md](CONTRIBUTING.md) for more details. See also the "Issues" tab.

