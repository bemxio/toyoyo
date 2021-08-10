import commands
import argparse

def main(path, debug=False):
    interpreter = commands.toyoyo
    interpreter.debug = debug

    interpreter.execute_many(path.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run a toyoyo script")
    parser.add_argument("path", help="path to the script", type=argparse.FileType("r"))
    parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true", default=False)

    args = vars(parser.parse_args())
    main(**args) 