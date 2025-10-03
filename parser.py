class InputParser:
    @staticmethod
    def parse_input_from_stdin(prompt):
        print(prompt)
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line.strip())
            else:
                break
        return lines

    @staticmethod
    def parse_input_from_file(filename):
        with open(filename) as inputFile:
            return [line.strip() for line in inputFile if line.strip()]