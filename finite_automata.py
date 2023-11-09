class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

    def read_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip().split()
                if line[0] == 'states':
                    self.states = set(line[1:])
                elif line[0] == 'alphabet':
                    self.alphabet = set(line[1:])
                elif line[0] == 'initial':
                    self.initial_state = line[1]
                elif line[0] == 'final':
                    self.final_states.add(line[1])
                elif line[0] == 'transitions':
                    for transition_line in file:
                        if not transition_line.strip():
                            break
                        transition = transition_line.strip().split()
                        current_state, symbol, next_state = transition
                        self.transitions[(current_state, symbol)] = next_state

    def display_elements(self):
        print("1. Set of States:", self.states)
        print("2. Alphabet:", self.alphabet)
        print("3. Transitions:")
        for transition, next_state in self.transitions.items():
            print(f"   {transition[0]} --({transition[1]})--> {next_state}")
        print("4. Initial State:", self.initial_state)
        print("5. Set of Final States:", self.final_states)

    def verify_sequence(self, sequence):
        current_state = self.initial_state
        for symbol in sequence:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.final_states


def main():
    fa = FiniteAutomaton()
    fa.read_from_file("fa1.txt")

    while True:
        print("\nMenu:")
        print("1. Display Elements")
        print("2. Verify Sequence (DFA only)")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            fa.display_elements()
        elif choice == '2':
            sequence = input("Enter the sequence to verify: ")
            result = fa.verify_sequence(sequence)
            if result:
                print("Sequence is accepted by the Finite Automaton.")
            else:
                print("Sequence is not accepted by the Finite Automaton.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
