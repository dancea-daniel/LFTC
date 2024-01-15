import prettytable
from prettytable import PrettyTable


class Grammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = dict()
        self.operations = list()

    def read_grammar_from_file(self, file_path):
        try:
            symbols = set()
            with open(file_path, 'r') as file:
                for line in file:
                    self.process_grammar_line(line.strip(), symbols)

            for symbol in symbols:
                if symbol not in self.nonterminals:
                    self.terminals.add(symbol)
            return True
        except Exception as e:
            print(f"Error reading grammar from file: {e}")
            return False

    def process_grammar_line(self, line, symbols_later):

        if not line or line.startswith('#'):
            return  # Ignore empty lines and comments

        parts = line.split('::=')
        if len(parts) != 2:
            print(f"Invalid production: {line}")
            return

        left_side = parts[0].strip()
        right_side = parts[1].strip()

        self.nonterminals.add(left_side)
        right_side = right_side.split("|")

        stripped_elements = [element.strip() for element in right_side]

        if left_side in self.productions:
            self.productions[left_side].extend(stripped_elements)
        else:
            self.productions[left_side] = stripped_elements

        for symbol in right_side:
            symbols_later.update(symbol.strip().split(' '))

        # if left_side in self.j:
        #     self.productions[left_side].append(symbols)
        # else:
        #     self.productions[left_side] = [symbols]

    def print_nonterminals(self):
        print("Nonterminals:", self.nonterminals)

    def print_terminals(self):
        print("Terminals:", self.terminals)

    def print_productions(self):
        print("Productions:")
        for key, value in self.productions.items():
            print(f"{key} -> {' | '.join(value)}")
        print("Terminals:", self.productions)

    def is_context_free(self):
        visited_non_terminal = set()
        is_changed = True
        while is_changed:
            is_changed = False
            for left_side, right_side in self.productions.items():
                # loop through the productions of a non-terminal
                if left_side not in visited_non_terminal:
                    for pr in right_side:
                        pr_set = pr.split(" ")
                        print(pr_set)
                        # loop through one of the productions
                        correct_pr = True
                        for word in pr_set:
                            if word in self.nonterminals:
                                if word not in visited_non_terminal:
                                    correct_pr = False
                                    break
                        if correct_pr:
                            visited_non_terminal.add(left_side)
                            is_changed = True
                            break

        return len(self.nonterminals) == len(visited_non_terminal)

    def goto(self, closure_list):
        # returns a set of the possible GOTOes for a given closure
        goto_set = set()
        for pr in closure_list:
            dot_index = pr.find('.')
            if dot_index != len(pr) - 1 and dot_index != -1:
                last_index = pr.find(" ", dot_index)
                if last_index == -1:
                    goto_set.add(pr[dot_index + 1:])
                else:
                    goto_set.add(pr[dot_index + 1:pr.find(" ", dot_index)])

        return goto_set

    def closure(self, way, closure_list, i0):
        new_closure_list = list()
        for cl in closure_list:
            # find .GOTO
            to_find = "." + way
            if to_find in cl:
                dot_index = cl.find(to_find)
                # switch dot
                if dot_index + len(to_find) < len(cl):
                    new_cl = cl[:dot_index] + way + " ." + cl[dot_index + len(to_find) + 1:]
                else:
                    new_cl = cl[:dot_index] + way + "." + cl[dot_index + len(to_find):]
                # add to the new closure
                new_closure_list.append(new_cl)

                # check if its a nonterminal and has a production
                new_way_index = new_cl.find(".")
                new_way = ""
                if new_way_index != -1:
                    end_new_way_index = new_cl.find(" ", new_way_index + 1)
                    if end_new_way_index == -1:
                        new_way = new_cl[new_way_index + 1:]
                    else:
                        new_way = new_cl[new_way_index + 1: end_new_way_index]

                # if it has, add a new closure
                if new_way != "":
                    new_non_terminal_to_add = set()
                    not_checked_non_terminals = set()
                    new_non_terminal_to_add.add(new_way)
                    old_left_side = new_way
                    changed = True
                    j = 0
                    while changed:
                        changed = False
                        for i in self.operations:
                            left_side, right_side = i.split("->")
                            if left_side in new_non_terminal_to_add and left_side not in not_checked_non_terminals:
                                tmp = right_side.split(' ')
                                changed = True
                                new_non_terminal_to_add.add(tmp[0][1:])
                                new_closure_list.append(i)
                                if left_side != old_left_side:
                                    not_checked_non_terminals.add(old_left_side)
                                    old_left_side = left_side
                        not_checked_non_terminals.add(old_left_side)
                        # if j == len(new_non_terminal_to_add) - 1:
                        #     break
                        # j += 1

                    # for i in self.operations:
                    #     left_side, right_side = i.split("->")
                    #     if left_side in new_non_terminal_to_add:
                    #         tmp = right_side.split(' ')
                    #         new_non_terminal_to_add.add(tmp[0][1:])
                    #         new_closure_list.append(i)

        return new_closure_list

    def canonical_collection(self):
        closure_list = list()
        # set up first closure with production item
        i0 = list()
        self.operations.append("X->.S")

        i0.append("X -> .S")
        tmp = set()
        tmp.add("S")
        for left_side, right_side in self.productions.items():
            if left_side in tmp:
                for pr in right_side:
                    tmp.add(pr.split(" ")[0])
                    i0.append(left_side + "->." + pr)

        print(f"i0: {i0}")

        for left_side, right_side in self.productions.items():
            for pr in right_side:
                self.operations .append(left_side + "->." + pr)

        closure_list.append(i0)
        print(f"base: {self.operations }")

        i = 0
        while True:
            # loop through the list and add new closures, stop when no new closure is found
            goto_set = self.goto(closure_list[i])
            for way in goto_set:
                new_closure_item = self.closure(way, closure_list[i], self.operations)
                if new_closure_item not in closure_list:
                    closure_list.append(new_closure_item)

            if i == len(closure_list) - 1:
                break
            i += 1

        return closure_list

    def create_action_parsing_table(self, closure_list):
        table = dict()
        for i in range(len(closure_list)):
            table[(i, "action")] = "shift"
            table[(i, "$")] = ""
            for terminal in self.terminals:
                table[(i, terminal)] = ""
            for non_terminal in self.nonterminals:
                table[(i, non_terminal)] = ""


        for i in range(len(closure_list)):
            is_shifted = False
            is_reduced = False
            for pr in closure_list[i]:
                if pr[0] == 'X' and i != 0:
                    table[(i, '$')] = "accept"
                    table[(i, "action")] = "accept"
                else:

                    # dark magic right here
                    dot_index = pr.find(".")

                    new_way = ""
                    terminal_index = ""
                    if dot_index < len(pr) - 1:
                        end_new_way_index = pr.find(" ", dot_index + 1)
                        if end_new_way_index == -1:
                            new_way = pr[:dot_index] + pr[dot_index + 1:] + "."
                            terminal_index = pr[dot_index + 1:]

                        else:
                            new_way = pr[:dot_index] + pr[dot_index + 1:end_new_way_index + 1] + "." + pr[end_new_way_index + 1:]
                            terminal_index = pr[dot_index + 1:end_new_way_index]
                    elif dot_index == len(pr) - 1:
                        is_reduced = True
                        leftside, rightside = pr.split('->')
                        new_word = leftside + "->." + rightside[:len(rightside) - 1]
                        index = self.operations.index(new_word)
                        table[(i, "action")] = "reduce " + str(index)

                    for j in range(len(closure_list)):
                        if new_way in closure_list[j]:
                            table[(i, terminal_index)] = j
                            is_shifted = True
                            break

                    if is_reduced and is_shifted:
                        raise Exception(f"Conflict error at closure: {closure_list[i]}")



        output_table = PrettyTable()

        # Define the columns using the second element of the tuples
        columns = set(key[1] for key in table.keys())
        output_table.field_names = ["Row", "action"] + list(sorted(columns - {"action"}))

        # Populate the table
        for row in set(key[0] for key in table.keys()):
            values = [table.get((row, "action"), "")] + [table.get((row, col), "") for col in
                                                         sorted(columns - {"action"})]
            output_table.add_row([row] + values)

        # Print the table
        print(output_table)

        return table

    def create_parsing_table(self, closure_list):
        table = dict()
        for i in range(len(closure_list)):
            for terminal in self.terminals:
                table[(i, terminal)] = ""
            for non_terminal in self.nonterminals:
                table[(i, non_terminal)] = ""
        for i in range(len(closure_list)):
            for pr in closure_list[i]:
                if pr[0] == 'X' and i != 0:
                    table[(i, 'S')] = "accept"

                # dark magic right here
                dot_index = pr.find(".")

                new_way = ""
                terminal_index = ""
                if dot_index < len(pr) - 1:
                    end_new_way_index = pr.find(" ", dot_index + 1)
                    if end_new_way_index == -1:
                        new_way = pr[:dot_index] + pr[dot_index + 1:] + "."
                        terminal_index = pr[dot_index + 1:]

                    else:
                        new_way = pr[:dot_index] + pr[dot_index + 1:end_new_way_index + 1] + "." + pr[end_new_way_index + 1:]
                        terminal_index = pr[dot_index + 1:end_new_way_index]

                for j in range(len(closure_list)):
                    if new_way in closure_list[j]:
                        if terminal_index in self.nonterminals:
                            table[(i, terminal_index)] = j
                        else:
                            table[(i, terminal_index)] = "S" + str(j)

        for i in range(len(closure_list)):
            is_zero = True
            for terminal in self.terminals:
                if table[(i, terminal)] != "":
                    is_zero = False
                    break
            for non_terminal in self.nonterminals:
                if table[(i, non_terminal)] != "":
                    is_zero = False
                    break

            if is_zero:
                leftside, rightside = closure_list[i][0].split("->")
                new_word = leftside + "->." + rightside[:len(rightside) - 1]
                index = self.operations.index(new_word)
                for terminal in self.terminals:
                    table[(i, terminal)] = "r" + str(index)

        output_table = PrettyTable()

        # Define the columns using the second element of the tuples
        columns = set(key[1] for key in table.keys())
        output_table.field_names = ["Row"] + list(sorted(columns))

        # Populate the table
        for row in set(key[0] for key in table.keys()):
            values = [table.get((row, col), "") for col in sorted(columns)]
            output_table.add_row([row] + values)

        # Print the table
        print(output_table)

    def parsing(self, ps_table, input_list):
        working_stack = []
        input_stack = []
        output_stack = []

        working_stack.append("$")
        working_stack.append("s0")
        input_stack.append("$")
        tree = []

        print(working_stack)

        for word in input_list:
            input_stack.insert(1, word)

        while True:
            current = input_stack.pop()
            op = int(working_stack[-1][1:])

            goto = ps_table[(op, current)]

            if type(goto) is int:
                working_stack.append(current)
                working_stack.append("s" + str(goto))
            elif "reduce" in ps_table[(op, "action")]:
                nr = int(ps_table[(op, "action")].split(" ")[1])
                output_stack.append(nr)
                input_stack.append(current)
                left_side, right_side = self.operations[nr].split("->")
                right_side_list = right_side[1:].split(" ")
                node = dict()
                node[left_side] = []
                for i in range(len(right_side_list)- 1, -1, -1):
                    print(i)
                    working_stack.pop()
                    working_stack.pop()
                    if right_side_list[i] in self.nonterminals:
                        for j in range(len(tree) - 1, -1, -1):
                            first_key = next(iter(tree[j]))
                            if first_key == right_side_list[i]:
                                node[left_side].insert(0, tree[j])
                                tree.remove(tree[j])
                                break
                    else:
                        node[left_side].insert(0, right_side_list[i])

                tree.append(node)

                op = int(working_stack[-1][1:])
                new_goto = ps_table[(op, left_side)]
                working_stack.append(left_side)
                working_stack.append("s" + str(new_goto))
            elif "accept" in ps_table[(op, "action")]:
                break

        print(f"working stack {working_stack}")
        print(f"input stack {input_stack}")
        print(f"output stack {output_stack}")
        print(f"tree: {tree}")

        return tree


grammar = Grammar()
grammar.read_grammar_from_file('g4.txt')
grammar.print_nonterminals()
grammar.print_terminals()
grammar.print_productions()
print(grammar.is_context_free())

closure_list = grammar.canonical_collection()
index = 0
for cl in closure_list:
    print(f"I{index}: {cl}")
    index += 1

# grammar.create_parsing_table(closure_list)
try:
    ps_table = grammar.create_action_parsing_table(closure_list)
    # grammar.parsing(ps_table, ["d", "d", "c", "c"])
except Exception as e:
    print(e)