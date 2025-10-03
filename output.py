class OutputGenerator:
    @staticmethod
    def print_recommendations(recommendations):
        for artist, score in recommendations.items():
            print(f"{artist}: {score}")

    @staticmethod
    def write_recommendations_to_file(recommendations, filename):
        import operator
        with open(filename, 'w') as f:
            sorted_recs = sorted(recommendations.items(), key=operator.itemgetter(1), reverse=True)
            for rec in sorted_recs:
                print(rec, file=f)

    @staticmethod
    def write_roots_to_file(roots, filename):
        with open(filename, 'w') as f:
            for root in sorted(roots.items(), key=lambda x: x[0]):
                print(root, file=f)
