import json
import requests
import operator
import urllib.parse
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
            apikey = (apikeyFile.readlines())[0].strip()
        for artist_name in self.startup_weights:
            encoded_artist_name = urllib.parse.quote(artist_name)
            similars_url = (
                "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar"
                + "&artist=" + encoded_artist_name + "&api_key=" + apikey + "&format=json"
            )
            try:
                similars_response = requests.get(similars_url)
                similars_response.raise_for_status()  # Raise an exception for bad status codes
                similars_data = similars_response.json()
                
                if 'similarartists' not in similars_data or 'artist' not in similars_data.get('similarartists', {}):
                    print(f"Warning: Could not find similar artists for '{artist_name}'. Skipping.")
                    continue

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
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {artist_name}: {e}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON for {artist_name}")
        return self.artist_recommendations, self.artist_roots


def run_recommendations(startup_weights, max_weight):
    """
    Runs the music recommendation process.
    
    Args:
        startup_weights (dict): A dictionary of artist names to their weights.
        max_weight (float): The maximum weight assigned to any artist.
        
    Returns:
        tuple: A tuple containing sorted artist recommendations and sorted artist roots.
    """
    recommender = MusicRecommender(startup_weights, max_weight)
    artist_recommendations, artist_roots = recommender.recommend()
    
    output_gen = OutputGenerator()
    sorted_artist_recommendations = sorted(artist_recommendations.items(), key=operator.itemgetter(1), reverse=True)
    output_gen.write_recommendations(sorted_artist_recommendations, filename='output.txt')
    
    sorted_artist_roots = sorted(artist_roots.items(), key=operator.itemgetter(0), reverse=False)
    output_gen.write_roots(sorted_artist_roots, filename='outroot.txt')
    
    return sorted_artist_recommendations, sorted_artist_roots


if __name__ == "__main__":
    cli_handler = CLIHandler()
    args = cli_handler.get_args()
    input_parser = InputParser(from_cli=args.i)
    startup_weights, max_weight = input_parser.parse(cli_handler=cli_handler if args.i else None)
    
    if startup_weights:
        print("Generating recommendations...")
        run_recommendations(startup_weights, max_weight)
        print("Recommendations written to output.txt and outroot.txt")
    else:
        print("No valid input artists provided. Exiting.")
