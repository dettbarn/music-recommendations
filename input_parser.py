class InputParser:
    def __init__(self, from_cli=False):
        self.from_cli = from_cli

    def _parse_lines(self, lines):
        startup_weights = {}
        max_weight = 0.0
        for line in lines:
            line = line.strip()
            if not line or '%' not in line:
                continue
            try:
                artist_name, weight_str = line.split('%', 1)
                weight = float(weight_str)
                startup_weights[artist_name.strip()] = weight
                if weight > max_weight:
                    max_weight = weight
            except (ValueError, IndexError):
                print(f"Warning: Skipping malformed line: '{line}'")
                continue
        return startup_weights, max_weight

    def parse_from_text(self, text_input):
        lines = text_input.strip().split('\n')
        return self._parse_lines(lines)

    def parse(self, cli_handler=None, input_file='input.txt'):
        if self.from_cli and cli_handler:
            lines = cli_handler.multiline_input("Enter the data : \n")
        else:
            try:
                with open(input_file) as inputFile:
                    lines = inputFile.readlines()
            except FileNotFoundError:
                print(f"Error: Input file not found at {input_file}")
                return {}, 0.0
        
        return self._parse_lines(lines)
