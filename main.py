import sys

from Parser import Parser
from TreePrinter import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "ex1"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    Parser = Parser()
    ast = Parser.run(text)
    if Parser.error or not Parser.parser.errorok:
        sys.exit(1)
    print(ast.printTree())
    print(ast.score)