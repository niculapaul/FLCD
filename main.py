from FiniteAutomata import *


def show_menu():
    print("=== Console ===\n"
          "1. Show States\n"
          "2. Show Alphabet\n"
          "3. Show Final States\n"
          "4. Show Transitions for a state\n"
          "5. Verify if a sequence is accepted by the FA\n"
          "0. Exit")


def run_menu(fa):
    options = [fa.show_states,
               fa.show_alphabet,
               fa.show_final_states,
               fa.show_transitions,
               fa.is_accepted]
    while True:
        show_menu()
        choice = int(input(">> "))
        if choice > len(options):
            print("Invalid command!\n")
        if choice == 0:
            return
        if choice <= 3:
            options[choice - 1]()
        else:
            argument = input(">>> ")
            options[choice - 1](argument)


if __name__ == '__main__':
    finite_automata = FiniteAutomata('fa.in')
    print(finite_automata)

    run_menu(finite_automata)
