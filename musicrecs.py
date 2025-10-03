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
from cli import CLI
from parser import InputParser
from recommender import Recommender
from output import OutputGenerator

if __name__ == "__main__":
    cli = CLI().get_args()
    cli_input = cli.i

    if cli_input:
        prompt = "Enter the data : \n"
        inp = InputParser.parse_input_from_stdin(prompt)
    else:
        inp = InputParser.parse_input_from_file('input.txt')

    # Parse input into a dictionary
    startup_weights = {}
    for line in inp:
        if '%' in line:
            artist_name, weight = line.split('%')
            startup_weights[artist_name] = float(weight)

    recommender = Recommender(startup_weights)
    recommender.calculate()

    OutputGenerator.write_recommendations_to_file(recommender.artist_recommendations, 'output.txt')
    OutputGenerator.write_roots_to_file(recommender.artist_roots, 'outroot.txt')
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
