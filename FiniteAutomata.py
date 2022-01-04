class FiniteAutomata:

    def __init__(self, file_name):
        with open(file_name) as file:
            self.Q = FiniteAutomata.parse_line(file.readline())
            self.E = FiniteAutomata.parse_line(file.readline())
            self.q0 = file.readline().split('=')[1].strip()
            self.F = FiniteAutomata.parse_line(file.readline())
            self.S = FiniteAutomata.parse_transitions(FiniteAutomata.parse_line(''.join([line for line in file])))

    def __str__(self):
        return 'Q = { ' + ', '.join(self.Q) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'F = { ' + ', '.join(self.F) + ' }\n' \
               + 'S = { ' + ', '.join([' -> '.join([str(part) for part in trans]) for trans in self.S]) + ' }\n' \
               + 'q0 = ' + str(self.q0) + '\n'
        # (('q1', '0'), 'q1')

    @staticmethod
    def parse_line(line):
        return [value.strip() for value in line.strip().split('=')[1].strip()[1:-1].strip().split(',')]


    @staticmethod
    def parse_transitions(parts):
        result = []
        transitions = []
        index = 0

        while index < len(parts):
            transitions.append(parts[index] + ',' + parts[index + 1])
            index += 2
        for transition in transitions:
            lhs, rhs = transition.split('->')
            state2 = rhs.strip()
            state1, route = [value.strip() for value in lhs.strip()[1:-1].split(',')]

            result.append(((state1, route), state2))

        return result

    def is_state(self, value):
        return value in self.Q

    def show_states(self):
        print(self.Q)

    def show_final_states(self):
        print(self.F)

    def show_alphabet(self):
        print(self.E)

    def get_transitions(self, state):
        if not self.is_state(state):
            raise Exception('Discovered an invalid state!')
        return [trans for trans in self.S if trans[0][0] == state]

    def show_transitions(self, state):
        transitions = self.get_transitions(state)
        print('{ \n  ' + '\n  '.join([' -> '.join([str(part) for part in trans]) for trans in transitions]) + '\n}')

    def is_dfa(self):
        heads = []
        for transition in self.S:
            if transition[0] in heads:
                return False
            heads.append(transition[0])
        return True

    def is_accepted(self, sequence):
        if self.is_dfa():
            state = self.q0
            for el in sequence:
                for transition in self.S:
                    if (state, el) == transition[0]:
                        state = transition[1]
                        break
            if state in self.F:
                print("Sequence is accepted")
                return True
            else:
                print("Sequence is NOT accepted")
                return False
        else:
            print("It is not a DFA!")
            return False


