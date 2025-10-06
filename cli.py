import argparse

class CLIHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description="CLI Input",
            allow_abbrev=True,
            add_help=True
        )
        self.parser.add_argument(
            "-i", help="input data from command line", action="store_true"
        )

    def get_args(self):
        return self.parser.parse_args()

    def multiline_input(self, prompt):
        print(prompt)
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line.strip())
            else:
                break
        return lines
