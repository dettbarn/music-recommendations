class Recommender:
    def __init__(self, startup_weights):
        self.startup_weights = startup_weights
        self.artist_recommendations = {}
        self.artist_roots = {}


    def calculate(self):
        import requests
        import json
        import operator
        max_weight = max(self.startup_weights.values()) if self.startup_weights else 1
        min_match = 0.3
        self.artist_recommendations = {}
        self.artist_roots = {}
        for artist_name in self.startup_weights:
            with open("./lastfm/.api_key") as apikeyFile:
                apikey = (apikeyFile.readlines())[0].strip()
            similars_url = (
                "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar"
                + "&artist=" + artist_name + "&api_key=" + apikey + "&format=json"
            )
            similars_response = requests.get(similars_url)
            similars_data = json.loads(similars_response.content)
            for similar_artist in similars_data.get('similarartists', {}).get('artist', []):
                similar_artist_name = similar_artist['name']
                match = similar_artist['match']
                if float(match) < min_match:
                    continue
                weight = float(match) * self.startup_weights[artist_name] / max_weight
                if similar_artist_name in self.artist_recommendations:
                    self.artist_recommendations[similar_artist_name] += weight
                    self.artist_roots[similar_artist_name] += (',' + artist_name + '(' + str(weight)
                                                           + ')(match' + str(match) + ')')
                else:
                    self.artist_recommendations[similar_artist_name] = weight
                    self.artist_roots[similar_artist_name] = artist_name + \
                        '(' + str(weight) + ')(match' + str(match) + ')'

    def get_recommendations(self):
        return self.artist_recommendations
