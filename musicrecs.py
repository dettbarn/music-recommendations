import json
import requests
import operator
import sys
import argparse


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="CLI Input", allow_abbrev=True, add_help=True)

        self.parser.add_argument(
            "-i", help="input data from command line", action="store_true")

    def get_args(self):
        return self.parser.parse_args()


def multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line.strip())
        else:
            break
    return lines


if __name__ == "__main__":

    startupWeights = {}
    startupScale = 1
    maxWeight = 0.

    cli = CLI().get_args()
    cli_input = cli.i

    if(cli_input):
        prompt = "Enter the data : \n"
        inp = multiline_input(prompt)
        for line in inp:
            (artistName, weight) = line.split('%')
            startupWeights[artistName] = float(weight)
            if float(weight) > maxWeight:
                maxWeight = float(weight)
    else:
        with open('input.txt') as inputFile:
            for line in inputFile:
                (artistName, weight) = line.split('%')
                startupWeights[artistName] = float(weight)
                if float(weight) > maxWeight:
                    maxWeight = float(weight)

    artistRecommendations = {}
    artistRoots = {}

    for artistName in startupWeights:
        minMatch = 0.3
        with open("./lastfm/.api_key") as apikeyFile:
            apikey = (apikeyFile.readlines())[0]
        similarsUrl = ("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar"
                       + "&artist=" + artistName + "&api_key=" + apikey + "&format=json")

        similarsResponse = requests.get(similarsUrl)
        similarsData = json.loads(similarsResponse.content)

        for similarArtist in similarsData['similarartists']['artist']:
            similarArtistName = similarArtist['name']
            match = similarArtist['match']
            if float(match) < minMatch:
                continue
            weight = float(match) * startupWeights[artistName] / maxWeight
            if similarArtistName in artistRecommendations:
                artistRecommendations[similarArtistName] += weight
                artistRoots[similarArtistName] += (',' + artistName + '(' + str(weight)
                                                   + ')(match' + str(match) + ')')
            else:
                artistRecommendations[similarArtistName] = weight
                artistRoots[similarArtistName] = artistName + \
                    '(' + str(weight) + ')(match' + str(match) + ')'

    artistRecommendationsFile = open('output.txt', 'w')
    sortedArtistRecommendations = sorted(artistRecommendations.items(),
                                         key=operator.itemgetter(1), reverse=True)
    for artistRecommendation in sortedArtistRecommendations:
        print(artistRecommendation, file=artistRecommendationsFile)

    artistRootsFile = open('outroot.txt', 'w')
    for artistRoot in sorted(artistRoots.items(),
                             key=operator.itemgetter(0), reverse=False):
        print(artistRoot, file=artistRootsFile)
