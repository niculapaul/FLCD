from Grammar import *


def read_grammar_from_file(in_file):
    with open(in_file, "r") as file:
        line = file.readline().strip()
        productions = []
        non_terminals = line.split(' ')
        line = file.readline().strip()
        terminals = line.split(' ')
        line = file.readline().strip()
        start_sym = line
        line = file.readline().strip()
        while line != "":
            segments = line.split('->')
            productions_on_line = segments[1].split('|')
            for prod in productions_on_line:
                production = Production(segments[0].replace(" ", ""), prod.split())
                productions.append(production)
            line = file.readline().strip()

        return Grammar(start_sym, terminals, non_terminals, productions)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gr = read_grammar_from_file('g1.txt')
