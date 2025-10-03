class InputParser:
    def __init__(self, from_cli=False):
        self.from_cli = from_cli

    def parse(self, cli_handler=None, input_file='input.txt'):
        startup_weights = {}
        max_weight = 0.0
        if self.from_cli and cli_handler:
            inp = cli_handler.multiline_input("Enter the data : \n")
            for line in inp:
                artist_name, weight = line.split('%')
                startup_weights[artist_name] = float(weight)
                if float(weight) > max_weight:
                    max_weight = float(weight)
        else:
            with open(input_file) as inputFile:
                for line in inputFile:
                    artist_name, weight = line.split('%')
                    startup_weights[artist_name] = float(weight)
                    if float(weight) > max_weight:
                        max_weight = float(weight)
        return startup_weights, max_weight
