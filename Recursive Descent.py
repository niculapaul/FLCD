from tree import TreeNode
from Config import *
from main import read_grammar_from_file
from tabulate import tabulate


class RecursiveDescentParser:

    def __init__(self, new_grammar, sequence):
        self.grammar = new_grammar
        self.config = Config(self.grammar.get_start_symbol())
        self.sequence = sequence

    def expand(self):
        #print("expand")
        #print(self.config)
        non_terminal = self.config.input_stack[0]
        first_prod = self.grammar.get_productions()[0].get_right_term()
        self.config.work_stack.append((non_terminal, 0))
        self.config.input_stack = first_prod + self.config.input_stack[1:]
        #print(self.config)

    def advance(self):
        #print("advance")
        #print(self.config)
        terminal = self.config.input_stack[0]
        self.config.index += 1
        self.config.work_stack.append(terminal)
        self.config.input_stack = self.config.input_stack[1:]
        #print(self.config)

    def momentaryInsuccess(self):
        #print("momentaryInsuccess")
        #print(self.config)
        self.config.state = State.BACK
        #print(self.config)

    def back(self):
        #print("back")
        #print(self.config)
        terminal = self.config.work_stack[-1]
        self.config.index -= 1
        self.config.work_stack.pop()
        self.config.input_stack = [terminal] + self.config.input_stack
        #print(self.config)

    def get_next_production(self, prod):
        for i in range(len(self.grammar.get_productions()) - 1):
            if self.grammar.productions[i].get_right_term() == prod \
                    and self.grammar.productions[i + 1].get_left_term() == self.grammar.productions[i].get_left_term():
                return self.grammar.productions[i + 1].get_right_term()
        return None

    def anotherTry(self):
        #print("anotherTry")
        #print(self.config)
        (non_terminal, last_prod_index) = self.config.work_stack.pop()
        last_production = self.grammar.get_productions()[last_prod_index].get_right_term()
        last_production_len = len(last_production)
        next_prod = self.get_next_production(last_production)
        if next_prod:
            self.config.state = State.NORMAL
            self.config.work_stack.append((non_terminal, last_prod_index + 1))
            self.config.input_stack = next_prod + self.config.input_stack[last_production_len:]
        elif self.config.index == 0 and non_terminal == self.grammar.get_start_symbol():
            self.config.state = State.ERROR
        else:
            self.config.input_stack = [non_terminal] + self.config.input_stack[last_production_len:]
        #print(self.config)

    def succes(self):
        #print("Succes")
        #print(self.config)
        self.config.state = State.FINAL
        #print(self.config)

    def parse_tree(self, workStack):
        currentIndex = 1
        firstNode = TreeNode(currentIndex, self.grammar.get_start_symbol(), 0, 0)
        treeNodes = [firstNode]
        for elem in workStack:
            if elem[0] not in self.grammar.get_non_terminals():
                currentIndex += 1
                continue
            elem = (elem[0], self.grammar.productions[elem[1]].get_right_term())
            if type(elem) is tuple and elem[0] in self.grammar.get_non_terminals():
                for symbol in range(len(elem[1])):
                    rightSibling = 0
                    if symbol > 0:
                        rightSibling = treeNodes[-1].index
                    treeNodes.append(TreeNode(len(treeNodes) + 1, elem[1][symbol], currentIndex, rightSibling))
            currentIndex += 1
        self.tree = [node.toList() for node in treeNodes]

    def recursive_descendent(self):

        while self.config.state != State.FINAL and self.config.state != State.ERROR:
            if self.config.state == State.NORMAL:
                if self.config.index == len(self.sequence) and len(self.config.input_stack) == 0:
                    self.succes()
                else:
                    if self.config.input_stack[0] in self.grammar.get_non_terminals():
                        self.expand()
                    else:
                        if self.config.index < len(self.sequence) and self.config.input_stack[0] == self.sequence[self.config.index]:
                            self.advance()
                        else:
                            self.momentaryInsuccess()
            else:
                if self.config.state == State.BACK:
                    if self.config.work_stack[-1] in self.grammar.get_terminals():
                        self.back()
                    else:
                        self.anotherTry()
        if self.config.state == State.ERROR:
            return False
        else:
            self.parse_tree(self.config.work_stack)
            return True


def read_sequence(filename):
    l = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        x = line.split(" ")
        l.append((x[0]))
    return l


if __name__ == "__main__":
    grammar = read_grammar_from_file("g1.txt")
    sequence = read_sequence("seq.txt")
    rdp = RecursiveDescendentParser(grammar, sequence)

    isValid = rdp.recursive_descendent()
    out = open("out1.txt", "w")
    if isValid:
        print("Sequence " + ''.join(sequence) + " is valid")
        out.write(tabulate(rdp.tree, numalign='center', tablefmt="pretty",
                           headers=['Index', 'Info', 'Parent', 'Left Sibling']))
    else:
        print("Sequence is not valid")
