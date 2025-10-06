import json
import requests
import operator
from cli import CLIHandler
from input_parser import InputParser
from output_generator import OutputGenerator


class MusicRecommender:
    def __init__(self, startup_weights, max_weight):
        self.startup_weights = startup_weights
        self.max_weight = max_weight
        self.artist_recommendations = {}
        self.artist_roots = {}

    def recommend(self):
        min_match = 0.3
        import os
        if not os.path.exists("./lastfm/.api_key"):
            print("[INFO] API key file not found. Skipping API calls. Returning empty recommendations for testing.")
            return self.artist_recommendations, self.artist_roots
        with open("./lastfm/.api_key") as apikeyFile:
            apikey = (apikeyFile.readlines())[0]
        for artist_name in self.startup_weights:
            similars_url = (
                "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar"
                + "&artist=" + artist_name + "&api_key=" + apikey + "&format=json"
            )
            similars_response = requests.get(similars_url)
            similars_data = json.loads(similars_response.content)
            for similar_artist in similars_data['similarartists']['artist']:
                similar_artist_name = similar_artist['name']
                match = similar_artist['match']
                if float(match) < min_match:
                    continue
                weight = float(match) * self.startup_weights[artist_name] / self.max_weight
                if similar_artist_name in self.artist_recommendations:
                    self.artist_recommendations[similar_artist_name] += weight
                    self.artist_roots[similar_artist_name] += (',' + artist_name + '(' + str(weight)
                                                           + ')(match' + str(match) + ')')
                else:
                    self.artist_recommendations[similar_artist_name] = weight
                    self.artist_roots[similar_artist_name] = artist_name + \
                        '(' + str(weight) + ')(match' + str(match) + ')'
        return self.artist_recommendations, self.artist_roots



if __name__ == "__main__":
    cli_handler = CLIHandler()
    args = cli_handler.get_args()
    input_parser = InputParser(from_cli=args.i)
    startup_weights, max_weight = input_parser.parse(cli_handler=cli_handler if args.i else None)
    recommender = MusicRecommender(startup_weights, max_weight)
    artist_recommendations, artist_roots = recommender.recommend()
    output_gen = OutputGenerator()
    sorted_artist_recommendations = sorted(artist_recommendations.items(), key=operator.itemgetter(1), reverse=True)
    output_gen.write_recommendations(sorted_artist_recommendations, filename='output.txt')
    sorted_artist_roots = sorted(artist_roots.items(), key=operator.itemgetter(0), reverse=False)
    output_gen.write_roots(sorted_artist_roots, filename='outroot.txt')
