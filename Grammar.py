class Production:
    def __init__(self, left_term, right_term):
        self.left_term = left_term
        self.right_term = right_term

    def get_left_term(self):
        return self.left_term

    def get_right_term(self):
        return self.right_term

    def set_left_term(self, new_left):
        self.left_term = new_left

    def set_right_term(self, new_right):
        self.right_term = new_right

    def __str__(self):
        right_str = "["
        for i in range(len(self.get_right_term())):
            if i != len(self.get_right_term()) - 1:
                right_str += self.get_right_term()[i] + ", "
            else:
                right_str += self.get_right_term()[i]
        right_str += "]"
        return self.left_term + " -> " + right_str


class Grammar:

    def __init__(self, start_symbol, terminals, non_terminals, productions):
        self.start_symbol = start_symbol
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions

    def get_start_symbol(self):
        return self.start_symbol

    def get_terminals(self):
        return self.terminals

    def get_non_terminals(self):
        return self.non_terminals

    def get_productions(self):
        return self.productions

    def set_start_symbol(self, new_sym):
        self.start_symbol = new_sym

    def set_terminals(self, new_terminals):
        self.terminals = new_terminals

    def set_non_terminals(self, new_non_term):
        self.non_terminals = new_non_term

    def set_productions(self, new_productions):
        self.productions = new_productions

    def is_terminal(self, symbol):
        return symbol in self.terminals

    def is_non_terminal(self, symbol):
        return symbol in self.non_terminals

    def __str__(self):
        string_prod = ""
        for prod in self.productions:
            string_prod += str(prod) + "\n"
        string_term = ""
        for term in self.terminals:
            string_term += term + " "
        string_non_term = ""
        for non_term in self.non_terminals:
            string_non_term += non_term + " "

        return "Start symbol: " + self.start_symbol + "\n" \
                "Terminals: " + string_term + "\n" \
                "Non-terminals: " + string_non_term + "\n" \
                "Productions:\n" + string_prod
