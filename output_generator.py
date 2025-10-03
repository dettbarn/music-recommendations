class OutputGenerator:
    def __init__(self):
        pass

    def write_recommendations(self, recommendations, filename='output.txt'):
        with open(filename, 'w') as f:
            for artist, weight in recommendations:
                print((artist, weight), file=f)

    def write_roots(self, roots, filename='outroot.txt'):
        with open(filename, 'w') as f:
            for artist, root in roots:
                print((artist, root), file=f)
